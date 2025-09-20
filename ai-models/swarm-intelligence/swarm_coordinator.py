"""
Multi-Agent Swarm Intelligence System
Implements advanced coordination algorithms for military vehicle swarms
including formation control, mission planning, and distributed decision making.
"""

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from collections import deque
import json
import logging
from datetime import datetime
import asyncio
from typing import List, Dict, Tuple, Optional, Any
import networkx as nx
from dataclasses import dataclass
import math
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Agent:
    """Individual agent in the swarm"""
    id: str
    position: np.ndarray
    velocity: np.ndarray
    heading: float
    role: str
    status: str
    capabilities: Dict[str, Any]
    communication_range: float
    max_speed: float
    energy: float
    equipment: List[str]

@dataclass
class Mission:
    """Mission definition for swarm operations"""
    id: str
    objective: str
    target_positions: List[np.ndarray]
    priority: int
    deadline: datetime
    formation_type: str
    required_agents: int
    risk_level: str

class SwarmIntelligenceNetwork(nn.Module):
    """Neural network for swarm decision making"""
    
    def __init__(self, input_size=20, hidden_size=128, output_size=10):
        super(SwarmIntelligenceNetwork, self).__init__()
        
        # Attention mechanism for agent communication
        self.attention = nn.MultiheadAttention(hidden_size, num_heads=8, batch_first=True)
        
        # Encoder for agent state
        self.agent_encoder = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size)
        )
        
        # Formation controller
        self.formation_controller = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 4)  # x, y, velocity, heading adjustments
        )
        
        # Decision network
        self.decision_network = nn.Sequential(
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, output_size),
            nn.Softmax(dim=-1)
        )
        
        # Communication network
        self.communication_net = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 32)  # Message encoding
        )
        
    def forward(self, agent_states, neighbor_states=None):
        # Encode agent states
        encoded_states = self.agent_encoder(agent_states)
        
        # If neighbors provided, use attention mechanism
        if neighbor_states is not None:
            neighbor_encoded = self.agent_encoder(neighbor_states)
            attended_features, _ = self.attention(encoded_states.unsqueeze(0), 
                                                neighbor_encoded, 
                                                neighbor_encoded)
            encoded_states = attended_features.squeeze(0)
        
        # Generate formation commands
        formation_commands = self.formation_controller(encoded_states)
        
        # Generate decisions
        combined_features = torch.cat([encoded_states, encoded_states.mean(dim=0, keepdim=True).expand_as(encoded_states)], dim=-1)
        decisions = self.decision_network(combined_features)
        
        # Generate communication messages
        messages = self.communication_net(encoded_states)
        
        return formation_commands, decisions, messages

class FormationController:
    """Advanced formation control algorithms"""
    
    def __init__(self):
        self.formation_types = {
            'line': self._line_formation,
            'wedge': self._wedge_formation,
            'diamond': self._diamond_formation,
            'circle': self._circle_formation,
            'echelon': self._echelon_formation,
            'column': self._column_formation,
            'box': self._box_formation
        }
        
    def calculate_formation_positions(self, formation_type: str, 
                                    center: np.ndarray, 
                                    num_agents: int, 
                                    spacing: float = 10.0,
                                    heading: float = 0.0) -> List[np.ndarray]:
        """Calculate target positions for formation"""
        if formation_type not in self.formation_types:
            formation_type = 'line'
        
        return self.formation_types[formation_type](center, num_agents, spacing, heading)
    
    def _line_formation(self, center, num_agents, spacing, heading):
        """Line formation - agents in a straight line"""
        positions = []
        start_offset = -(num_agents - 1) * spacing / 2
        
        for i in range(num_agents):
            offset = start_offset + i * spacing
            # Perpendicular to heading direction
            perp_heading = heading + np.pi/2
            pos = center + np.array([offset * np.cos(perp_heading), 
                                   offset * np.sin(perp_heading)])
            positions.append(pos)
        
        return positions
    
    def _wedge_formation(self, center, num_agents, spacing, heading):
        """V-shaped wedge formation"""
        positions = [center]  # Leader at center
        
        for i in range(1, num_agents):
            side = 1 if i % 2 == 1 else -1
            rank = (i + 1) // 2
            
            # Calculate position behind and to the side of leader
            x_offset = -rank * spacing * np.cos(heading)
            y_offset = side * rank * spacing * 0.7 * np.sin(heading + np.pi/2)
            
            pos = center + np.array([x_offset, y_offset])
            positions.append(pos)
        
        return positions
    
    def _diamond_formation(self, center, num_agents, spacing, heading):
        """Diamond formation for small groups"""
        if num_agents < 4:
            return self._line_formation(center, num_agents, spacing, heading)
        
        positions = []
        
        # Center agent
        positions.append(center)
        
        if num_agents > 1:
            # Front agent
            front_pos = center + spacing * np.array([np.cos(heading), np.sin(heading)])
            positions.append(front_pos)
        
        if num_agents > 2:
            # Left agent
            left_pos = center + spacing * np.array([np.cos(heading + np.pi/2), np.sin(heading + np.pi/2)])
            positions.append(left_pos)
        
        if num_agents > 3:
            # Right agent
            right_pos = center + spacing * np.array([np.cos(heading - np.pi/2), np.sin(heading - np.pi/2)])
            positions.append(right_pos)
        
        # Additional agents in expanded diamond
        for i in range(4, num_agents):
            angle = heading + (i - 4) * 2 * np.pi / max(1, num_agents - 4)
            pos = center + spacing * 1.5 * np.array([np.cos(angle), np.sin(angle)])
            positions.append(pos)
        
        return positions
    
    def _circle_formation(self, center, num_agents, spacing, heading):
        """Circular formation"""
        positions = []
        radius = spacing * num_agents / (2 * np.pi)
        
        for i in range(num_agents):
            angle = heading + i * 2 * np.pi / num_agents
            pos = center + radius * np.array([np.cos(angle), np.sin(angle)])
            positions.append(pos)
        
        return positions
    
    def _echelon_formation(self, center, num_agents, spacing, heading):
        """Echelon formation - diagonal line"""
        positions = []
        
        for i in range(num_agents):
            x_offset = -i * spacing * 0.7 * np.cos(heading)
            y_offset = -i * spacing * 0.7 * np.sin(heading + np.pi/4)
            
            pos = center + np.array([x_offset, y_offset])
            positions.append(pos)
        
        return positions
    
    def _column_formation(self, center, num_agents, spacing, heading):
        """Column formation - single file"""
        positions = []
        
        for i in range(num_agents):
            offset = -i * spacing
            pos = center + offset * np.array([np.cos(heading), np.sin(heading)])
            positions.append(pos)
        
        return positions
    
    def _box_formation(self, center, num_agents, spacing, heading):
        """Box/square formation"""
        positions = []
        side_length = int(np.ceil(np.sqrt(num_agents)))
        
        for i in range(num_agents):
            row = i // side_length
            col = i % side_length
            
            x_offset = (col - side_length/2) * spacing
            y_offset = (row - side_length/2) * spacing
            
            # Rotate based on heading
            rotated_x = x_offset * np.cos(heading) - y_offset * np.sin(heading)
            rotated_y = x_offset * np.sin(heading) + y_offset * np.cos(heading)
            
            pos = center + np.array([rotated_x, rotated_y])
            positions.append(pos)
        
        return positions

class SwarmCoordinator:
    """Main swarm coordination system"""
    
    def __init__(self, max_agents=50):
        self.agents: Dict[str, Agent] = {}
        self.missions: Dict[str, Mission] = {}
        self.formation_controller = FormationController()
        self.communication_graph = nx.Graph()
        
        # AI network for decision making
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.swarm_network = SwarmIntelligenceNetwork().to(self.device)
        
        # Coordination parameters
        self.coordination_params = {
            'max_communication_range': 100.0,
            'collision_avoidance_distance': 5.0,
            'formation_tolerance': 2.0,
            'update_frequency': 10.0,  # Hz
            'consensus_threshold': 0.7
        }
        
        # Performance metrics
        self.metrics = {
            'formation_error': 0.0,
            'communication_efficiency': 0.0,
            'mission_progress': 0.0,
            'energy_consumption': 0.0,
            'collision_count': 0
        }
        
        logger.info("Swarm Coordinator initialized")
    
    def add_agent(self, agent: Agent):
        """Add agent to swarm"""
        self.agents[agent.id] = agent
        self.communication_graph.add_node(agent.id)
        logger.info(f"Agent {agent.id} added to swarm")
    
    def remove_agent(self, agent_id: str):
        """Remove agent from swarm"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.communication_graph.remove_node(agent_id)
            logger.info(f"Agent {agent_id} removed from swarm")
    
    def create_mission(self, mission: Mission):
        """Create new mission for swarm"""
        self.missions[mission.id] = mission
        logger.info(f"Mission {mission.id} created: {mission.objective}")
    
    def update_communication_graph(self):
        """Update communication connectivity between agents"""
        self.communication_graph.clear_edges()
        
        agents_list = list(self.agents.values())
        for i, agent1 in enumerate(agents_list):
            for agent2 in agents_list[i+1:]:
                distance = np.linalg.norm(agent1.position - agent2.position)
                max_range = min(agent1.communication_range, agent2.communication_range)
                
                if distance <= max_range:
                    self.communication_graph.add_edge(agent1.id, agent2.id, 
                                                    weight=1.0 / (distance + 0.1))
    
    def calculate_swarm_state(self) -> Dict[str, Any]:
        """Calculate overall swarm state"""
        if not self.agents:
            return {}
        
        positions = np.array([agent.position for agent in self.agents.values()])
        velocities = np.array([agent.velocity for agent in self.agents.values()])
        
        center_of_mass = np.mean(positions, axis=0)
        avg_velocity = np.mean(velocities, axis=0)
        spread = np.std(positions, axis=0)
        
        return {
            'center_of_mass': center_of_mass,
            'average_velocity': avg_velocity,
            'spread': spread,
            'num_agents': len(self.agents),
            'connectivity': nx.average_clustering(self.communication_graph),
            'avg_energy': np.mean([agent.energy for agent in self.agents.values()])
        }
    
    def plan_formation_transition(self, target_formation: str, 
                                center: np.ndarray, 
                                spacing: float = 10.0,
                                heading: float = 0.0) -> Dict[str, np.ndarray]:
        """Plan transition to target formation"""
        agents_list = list(self.agents.values())
        num_agents = len(agents_list)
        
        if num_agents == 0:
            return {}
        
        # Calculate target positions
        target_positions = self.formation_controller.calculate_formation_positions(
            target_formation, center, num_agents, spacing, heading
        )
        
        # Assign agents to positions (minimize total movement)
        assignments = self._optimize_position_assignments(agents_list, target_positions)
        
        return assignments
    
    def _optimize_position_assignments(self, agents: List[Agent], 
                                     target_positions: List[np.ndarray]) -> Dict[str, np.ndarray]:
        """Optimize assignment of agents to target positions"""
        # Simple greedy assignment - can be improved with Hungarian algorithm
        assignments = {}
        available_positions = target_positions.copy()
        
        # Sort agents by their distance to center
        center = np.mean(target_positions, axis=0)
        agents_sorted = sorted(agents, key=lambda a: np.linalg.norm(a.position - center))
        
        for agent in agents_sorted:
            if not available_positions:
                break
            
            # Find closest available position
            distances = [np.linalg.norm(agent.position - pos) for pos in available_positions]
            closest_idx = np.argmin(distances)
            
            assignments[agent.id] = available_positions.pop(closest_idx)
        
        return assignments
    
    def execute_formation_transition(self, assignments: Dict[str, np.ndarray]):
        """Execute formation transition with collision avoidance"""
        for agent_id, target_pos in assignments.items():
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                
                # Calculate desired velocity towards target
                direction = target_pos - agent.position
                distance = np.linalg.norm(direction)
                
                if distance > self.coordination_params['formation_tolerance']:
                    desired_velocity = direction / distance * agent.max_speed
                    
                    # Apply collision avoidance
                    avoidance_force = self._calculate_collision_avoidance(agent)
                    
                    # Combine forces
                    final_velocity = desired_velocity + avoidance_force
                    final_velocity = np.clip(np.linalg.norm(final_velocity), 0, agent.max_speed) * \
                                   final_velocity / (np.linalg.norm(final_velocity) + 1e-8)
                    
                    # Update agent
                    agent.velocity = final_velocity
                    agent.position += agent.velocity * (1.0 / self.coordination_params['update_frequency'])
                    agent.heading = np.arctan2(final_velocity[1], final_velocity[0])
    
    def _calculate_collision_avoidance(self, agent: Agent) -> np.ndarray:
        """Calculate collision avoidance force for agent"""
        avoidance_force = np.zeros(2)
        
        for other_agent in self.agents.values():
            if other_agent.id == agent.id:
                continue
            
            relative_pos = agent.position - other_agent.position
            distance = np.linalg.norm(relative_pos)
            
            if distance < self.coordination_params['collision_avoidance_distance']:
                # Repulsive force inversely proportional to distance
                if distance > 0:
                    force_magnitude = (self.coordination_params['collision_avoidance_distance'] - distance) / distance
                    avoidance_force += force_magnitude * relative_pos / distance
        
        return avoidance_force
    
    def coordinate_mission_execution(self, mission_id: str):
        """Coordinate execution of specific mission"""
        if mission_id not in self.missions:
            logger.error(f"Mission {mission_id} not found")
            return
        
        mission = self.missions[mission_id]
        
        # Assign agents to mission based on capabilities and proximity
        assigned_agents = self._assign_agents_to_mission(mission)
        
        # Plan formation for mission
        if mission.target_positions:
            target_center = np.mean(mission.target_positions, axis=0)
            assignments = self.plan_formation_transition(
                mission.formation_type, target_center
            )
            
            # Execute formation transition
            self.execute_formation_transition(assignments)
        
        # Update mission progress
        self._update_mission_progress(mission_id)
        
        logger.info(f"Coordinating mission {mission_id} with {len(assigned_agents)} agents")
    
    def _assign_agents_to_mission(self, mission: Mission) -> List[str]:
        """Assign best agents to mission based on capabilities"""
        # Score agents based on suitability for mission
        agent_scores = {}
        
        for agent_id, agent in self.agents.items():
            score = 0.0
            
            # Distance to target (closer is better)
            if mission.target_positions:
                min_distance = min([np.linalg.norm(agent.position - target) 
                                  for target in mission.target_positions])
                score += 1.0 / (min_distance + 1.0)
            
            # Energy level
            score += agent.energy / 100.0
            
            # Role match (simplified)
            if mission.objective.lower() in agent.role.lower():
                score += 2.0
            
            # Equipment match
            if any(eq in mission.objective.lower() for eq in agent.equipment):
                score += 1.0
            
            agent_scores[agent_id] = score
        
        # Select top agents
        sorted_agents = sorted(agent_scores.keys(), key=lambda x: agent_scores[x], reverse=True)
        return sorted_agents[:mission.required_agents]
    
    def _update_mission_progress(self, mission_id: str):
        """Update mission progress based on agent positions"""
        mission = self.missions[mission_id]
        
        if not mission.target_positions:
            return
        
        # Calculate how close agents are to target positions
        total_distance = 0
        assigned_agents = self._assign_agents_to_mission(mission)
        
        for agent_id in assigned_agents:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                min_distance = min([np.linalg.norm(agent.position - target) 
                                  for target in mission.target_positions])
                total_distance += min_distance
        
        # Progress inversely related to total distance
        if assigned_agents:
            avg_distance = total_distance / len(assigned_agents)
            progress = max(0, 1.0 - avg_distance / 100.0)  # Assume 100m is max meaningful distance
            self.metrics['mission_progress'] = progress
    
    def implement_consensus_algorithm(self, variable_name: str, 
                                    initial_values: Dict[str, float]) -> float:
        """Implement distributed consensus algorithm"""
        # Initialize values for each agent
        current_values = initial_values.copy()
        max_iterations = 100
        convergence_threshold = 0.01
        
        for iteration in range(max_iterations):
            new_values = {}
            
            for agent_id in current_values:
                if agent_id not in self.agents:
                    continue
                
                # Get neighbors from communication graph
                neighbors = list(self.communication_graph.neighbors(agent_id))
                
                if not neighbors:
                    new_values[agent_id] = current_values[agent_id]
                    continue
                
                # Average with neighbors (basic consensus)
                neighbor_values = [current_values.get(neighbor, current_values[agent_id]) 
                                 for neighbor in neighbors]
                avg_value = (current_values[agent_id] + sum(neighbor_values)) / (len(neighbor_values) + 1)
                new_values[agent_id] = avg_value
            
            # Check convergence
            max_change = max([abs(new_values[aid] - current_values[aid]) 
                            for aid in current_values if aid in new_values])
            
            if max_change < convergence_threshold:
                logger.info(f"Consensus reached for {variable_name} in {iteration} iterations")
                break
            
            current_values = new_values
        
        # Return consensus value
        if new_values:
            return sum(new_values.values()) / len(new_values)
        return 0.0
    
    def predict_swarm_behavior(self, time_horizon: float = 10.0) -> Dict[str, Any]:
        """Predict future swarm behavior using AI model"""
        if not self.agents:
            return {}
        
        # Prepare input features
        agent_features = []
        for agent in self.agents.values():
            features = np.concatenate([
                agent.position,
                agent.velocity,
                [agent.heading, agent.energy / 100.0],
                np.zeros(14)  # Padding to match network input size
            ])[:20]
            agent_features.append(features)
        
        agent_states = torch.FloatTensor(agent_features).to(self.device)
        
        # Get predictions from neural network
        with torch.no_grad():
            formation_commands, decisions, messages = self.swarm_network(agent_states)
        
        # Interpret predictions
        predictions = {
            'predicted_positions': {},
            'formation_adjustments': formation_commands.cpu().numpy(),
            'decision_probabilities': decisions.cpu().numpy(),
            'communication_messages': messages.cpu().numpy(),
            'time_horizon': time_horizon
        }
        
        # Predict future positions based on current velocity
        for i, agent in enumerate(self.agents.values()):
            future_pos = agent.position + agent.velocity * time_horizon
            predictions['predicted_positions'][agent.id] = future_pos
        
        return predictions
    
    def optimize_swarm_parameters(self):
        """Optimize swarm coordination parameters using performance metrics"""
        # Simple optimization based on recent performance
        if self.metrics['formation_error'] > 5.0:
            self.coordination_params['formation_tolerance'] *= 1.1
        elif self.metrics['formation_error'] < 1.0:
            self.coordination_params['formation_tolerance'] *= 0.95
        
        if self.metrics['collision_count'] > 0:
            self.coordination_params['collision_avoidance_distance'] *= 1.2
        
        # Update communication range based on connectivity
        if self.metrics['communication_efficiency'] < 0.5:
            self.coordination_params['max_communication_range'] *= 1.1
    
    def generate_swarm_report(self) -> Dict[str, Any]:
        """Generate comprehensive swarm status report"""
        swarm_state = self.calculate_swarm_state()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'swarm_state': swarm_state,
            'agent_count': len(self.agents),
            'active_missions': len(self.missions),
            'communication_connectivity': nx.average_clustering(self.communication_graph) if self.agents else 0,
            'performance_metrics': self.metrics.copy(),
            'coordination_parameters': self.coordination_params.copy(),
            'agent_status': {
                agent_id: {
                    'position': agent.position.tolist(),
                    'velocity': agent.velocity.tolist(),
                    'heading': agent.heading,
                    'energy': agent.energy,
                    'status': agent.status,
                    'role': agent.role
                }
                for agent_id, agent in self.agents.items()
            }
        }
        
        return report

def create_sample_swarm(num_agents: int = 10) -> SwarmCoordinator:
    """Create a sample swarm for testing"""
    coordinator = SwarmCoordinator()
    
    # Create sample agents
    for i in range(num_agents):
        agent = Agent(
            id=f"agent_{i:03d}",
            position=np.random.uniform(-50, 50, 2),
            velocity=np.random.uniform(-2, 2, 2),
            heading=np.random.uniform(0, 2*np.pi),
            role=random.choice(['scout', 'assault', 'support', 'command']),
            status='active',
            capabilities={'navigation': True, 'communication': True, 'combat': True},
            communication_range=30.0,
            max_speed=10.0,
            energy=random.uniform(70, 100),
            equipment=random.sample(['radar', 'weapons', 'medical', 'repair'], 2)
        )
        coordinator.add_agent(agent)
    
    # Create sample mission
    mission = Mission(
        id="patrol_001",
        objective="Patrol designated area and secure perimeter",
        target_positions=[np.array([0, 0]), np.array([50, 50])],
        priority=1,
        deadline=datetime.now(),
        formation_type='line',
        required_agents=8,
        risk_level='medium'
    )
    coordinator.create_mission(mission)
    
    return coordinator

# Example usage and testing
if __name__ == "__main__":
    # Create sample swarm
    swarm = create_sample_swarm(15)
    
    # Update communication graph
    swarm.update_communication_graph()
    
    # Plan formation transition
    target_center = np.array([25, 25])
    assignments = swarm.plan_formation_transition('wedge', target_center, spacing=8.0)
    
    # Execute formation transition
    swarm.execute_formation_transition(assignments)
    
    # Coordinate mission execution
    swarm.coordinate_mission_execution('patrol_001')
    
    # Generate behavior predictions
    predictions = swarm.predict_swarm_behavior(time_horizon=5.0)
    
    # Implement consensus algorithm
    initial_values = {agent_id: np.random.uniform(0, 10) for agent_id in swarm.agents.keys()}
    consensus_value = swarm.implement_consensus_algorithm('target_speed', initial_values)
    
    # Generate comprehensive report
    report = swarm.generate_swarm_report()
    
    print("Swarm Intelligence System Report:")
    print(json.dumps(report, indent=2, default=str))
    
    logger.info("Swarm intelligence system test completed successfully")