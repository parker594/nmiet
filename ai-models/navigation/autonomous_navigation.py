"""
Advanced Autonomous Navigation System for Military Vehicles
Uses Deep Q-Network (DQN) with prioritized experience replay
for GPS-denied terrain navigation and obstacle avoidance.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
from collections import deque, namedtuple
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Transition tuple for experience replay
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'done'))

class PrioritizedReplayBuffer:
    """Prioritized Experience Replay Buffer for improved learning efficiency"""
    
    def __init__(self, capacity=100000, alpha=0.6, beta=0.4):
        self.capacity = capacity
        self.alpha = alpha
        self.beta = beta
        self.buffer = []
        self.priorities = np.zeros((capacity,), dtype=np.float32)
        self.position = 0
        
    def add(self, state, action, next_state, reward, done):
        """Add experience to buffer with maximum priority"""
        max_priority = self.priorities.max() if self.buffer else 1.0
        
        if len(self.buffer) < self.capacity:
            self.buffer.append(Transition(state, action, next_state, reward, done))
        else:
            self.buffer[self.position] = Transition(state, action, next_state, reward, done)
            
        self.priorities[self.position] = max_priority
        self.position = (self.position + 1) % self.capacity
        
    def sample(self, batch_size):
        """Sample batch with prioritized probabilities"""
        if len(self.buffer) == self.capacity:
            priorities = self.priorities
        else:
            priorities = self.priorities[:self.position]
            
        probabilities = priorities ** self.alpha
        probabilities /= probabilities.sum()
        
        indices = np.random.choice(len(self.buffer), batch_size, p=probabilities)
        samples = [self.buffer[idx] for idx in indices]
        
        # Importance sampling weights
        total = len(self.buffer)
        weights = (total * probabilities[indices]) ** (-self.beta)
        weights /= weights.max()
        
        return samples, indices, torch.FloatTensor(weights)
        
    def update_priorities(self, indices, priorities):
        """Update priorities of sampled experiences"""
        for idx, priority in zip(indices, priorities):
            self.priorities[idx] = priority
            
    def __len__(self):
        return len(self.buffer)

class DQNNetwork(nn.Module):
    """Deep Q-Network for navigation decision making"""
    
    def __init__(self, state_size, action_size, hidden_size=512):
        super(DQNNetwork, self).__init__()
        
        # Convolutional layers for spatial feature extraction
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        
        # Calculate conv output size
        conv_out_size = self._get_conv_out_size(state_size)
        
        # Fully connected layers
        self.fc1 = nn.Linear(conv_out_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)
        
        # Dueling DQN architecture
        self.value_stream = nn.Linear(hidden_size, 1)
        self.advantage_stream = nn.Linear(hidden_size, action_size)
        
        self.dropout = nn.Dropout(0.2)
        
    def _get_conv_out_size(self, shape):
        """Calculate output size of convolutional layers"""
        x = torch.zeros(1, *shape)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        return int(np.prod(x.size()))
        
    def forward(self, x):
        """Forward pass through the network"""
        # Convolutional feature extraction
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        
        # Flatten for fully connected layers
        x = x.view(x.size(0), -1)
        
        # Shared layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        
        # Dueling streams
        value = self.value_stream(x)
        advantage = self.advantage_stream(x)
        
        # Combine value and advantage
        q_values = value + (advantage - advantage.mean(dim=1, keepdim=True))
        
        return q_values

class AutonomousNavigationAgent:
    """Advanced DQN Agent for autonomous military vehicle navigation"""
    
    def __init__(self, state_size, action_size, config=None):
        self.state_size = state_size
        self.action_size = action_size
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Hyperparameters
        self.config = config or {
            'learning_rate': 1e-4,
            'gamma': 0.99,
            'epsilon': 1.0,
            'epsilon_min': 0.01,
            'epsilon_decay': 0.995,
            'batch_size': 32,
            'update_target_freq': 1000,
            'memory_size': 100000
        }
        
        # Neural networks
        self.q_network = DQNNetwork(state_size, action_size).to(self.device)
        self.target_network = DQNNetwork(state_size, action_size).to(self.device)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=self.config['learning_rate'])
        
        # Experience replay
        self.memory = PrioritizedReplayBuffer(self.config['memory_size'])
        
        # Training variables
        self.step_count = 0
        self.epsilon = self.config['epsilon']
        
        # Performance tracking
        self.training_history = {
            'losses': [],
            'rewards': [],
            'epsilon_values': [],
            'q_values': []
        }
        
        logger.info(f"Initialized AutonomousNavigationAgent on {self.device}")
        
    def get_action(self, state, training=True):
        """Select action using epsilon-greedy policy"""
        if training and random.random() < self.epsilon:
            return random.randrange(self.action_size)
        
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state)
        
        # Store Q-values for analysis
        self.training_history['q_values'].append(q_values.mean().item())
        
        return q_values.argmax().item()
    
    def store_experience(self, state, action, next_state, reward, done):
        """Store experience in replay buffer"""
        self.memory.add(state, action, next_state, reward, done)
    
    def train(self):
        """Train the agent using prioritized experience replay"""
        if len(self.memory) < self.config['batch_size']:
            return
        
        # Sample batch from memory
        batch, indices, weights = self.memory.sample(self.config['batch_size'])
        states = torch.FloatTensor([e.state for e in batch]).to(self.device)
        actions = torch.LongTensor([e.action for e in batch]).to(self.device)
        next_states = torch.FloatTensor([e.next_state for e in batch]).to(self.device)
        rewards = torch.FloatTensor([e.reward for e in batch]).to(self.device)
        dones = torch.BoolTensor([e.done for e in batch]).to(self.device)
        weights = weights.to(self.device)
        
        # Current Q-values
        current_q_values = self.q_network(states).gather(1, actions.unsqueeze(1))
        
        # Next Q-values using target network (Double DQN)
        next_actions = self.q_network(next_states).argmax(1).unsqueeze(1)
        next_q_values = self.target_network(next_states).gather(1, next_actions).detach()
        
        # Target Q-values
        target_q_values = rewards.unsqueeze(1) + (self.config['gamma'] * next_q_values * (~dones).unsqueeze(1))
        
        # Calculate loss with importance sampling weights
        td_errors = target_q_values - current_q_values
        loss = (weights.unsqueeze(1) * F.mse_loss(current_q_values, target_q_values, reduction='none')).mean()
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), 1.0)
        self.optimizer.step()
        
        # Update priorities
        priorities = np.abs(td_errors.detach().cpu().numpy()) + 1e-6
        self.memory.update_priorities(indices, priorities.flatten())
        
        # Update target network
        self.step_count += 1
        if self.step_count % self.config['update_target_freq'] == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())
        
        # Decay epsilon
        if self.epsilon > self.config['epsilon_min']:
            self.epsilon *= self.config['epsilon_decay']
        
        # Store training metrics
        self.training_history['losses'].append(loss.item())
        self.training_history['epsilon_values'].append(self.epsilon)
        
        return loss.item()
    
    def save_model(self, filepath):
        """Save model and training state"""
        torch.save({
            'q_network_state': self.q_network.state_dict(),
            'target_network_state': self.target_network.state_dict(),
            'optimizer_state': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'step_count': self.step_count,
            'config': self.config,
            'training_history': self.training_history
        }, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load model and training state"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.q_network.load_state_dict(checkpoint['q_network_state'])
        self.target_network.load_state_dict(checkpoint['target_network_state'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state'])
        self.epsilon = checkpoint['epsilon']
        self.step_count = checkpoint['step_count']
        self.training_history = checkpoint['training_history']
        logger.info(f"Model loaded from {filepath}")
    
    def get_navigation_decision(self, terrain_data, current_position, target_position, threats=None):
        """
        Make navigation decision based on terrain and threat analysis
        
        Args:
            terrain_data: 2D array of terrain elevation and obstacles
            current_position: (x, y) current coordinates
            target_position: (x, y) target coordinates
            threats: List of threat positions and types
        
        Returns:
            dict: Navigation decision with action, confidence, and reasoning
        """
        # Preprocess state
        state = self._preprocess_state(terrain_data, current_position, target_position, threats)
        
        # Get action from trained model
        action = self.get_action(state, training=False)
        
        # Get Q-values for confidence estimation
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        q_values = self.q_network(state_tensor).detach().cpu().numpy()[0]
        
        # Map action to movement
        action_map = {
            0: 'NORTH',
            1: 'SOUTH', 
            2: 'EAST',
            3: 'WEST',
            4: 'NORTHEAST',
            5: 'NORTHWEST',
            6: 'SOUTHEAST',
            7: 'SOUTHWEST',
            8: 'WAIT'
        }
        
        confidence = np.max(q_values) / (np.sum(np.abs(q_values)) + 1e-8)
        
        return {
            'action': action_map.get(action, 'WAIT'),
            'confidence': float(confidence),
            'q_values': q_values.tolist(),
            'reasoning': self._generate_reasoning(state, action, q_values),
            'threat_assessment': self._assess_threats(threats, current_position),
            'estimated_time': self._estimate_travel_time(current_position, target_position),
            'risk_level': self._calculate_risk_level(state, threats)
        }
    
    def _preprocess_state(self, terrain_data, current_pos, target_pos, threats):
        """Preprocess environment data into neural network input"""
        # Create multi-channel state representation
        height, width = terrain_data.shape
        state = np.zeros((4, height, width), dtype=np.float32)
        
        # Channel 0: Normalized terrain elevation
        state[0] = (terrain_data - terrain_data.min()) / (terrain_data.max() - terrain_data.min() + 1e-8)
        
        # Channel 1: Current position
        if 0 <= current_pos[0] < height and 0 <= current_pos[1] < width:
            state[1, current_pos[0], current_pos[1]] = 1.0
        
        # Channel 2: Target position
        if 0 <= target_pos[0] < height and 0 <= target_pos[1] < width:
            state[2, target_pos[0], target_pos[1]] = 1.0
        
        # Channel 3: Threat map
        if threats:
            for threat in threats:
                if 'position' in threat:
                    tx, ty = threat['position']
                    if 0 <= tx < height and 0 <= ty < width:
                        threat_intensity = threat.get('intensity', 1.0)
                        state[3, tx, ty] = threat_intensity
        
        return state
    
    def _generate_reasoning(self, state, action, q_values):
        """Generate human-readable reasoning for the decision"""
        action_names = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'NORTHEAST', 'NORTHWEST', 'SOUTHEAST', 'SOUTHWEST', 'WAIT']
        
        reasoning = f"Selected {action_names[action]} based on terrain analysis. "
        
        # Analyze Q-values
        best_actions = np.argsort(q_values)[-3:][::-1]
        reasoning += f"Top alternatives: {', '.join([action_names[a] for a in best_actions])}. "
        
        # Threat considerations
        threat_level = np.mean(state[3])
        if threat_level > 0.3:
            reasoning += "High threat environment detected - prioritizing evasive maneuvers. "
        elif threat_level > 0.1:
            reasoning += "Moderate threats present - maintaining cautious advancement. "
        else:
            reasoning += "Low threat environment - optimizing for speed and efficiency. "
        
        return reasoning
    
    def _assess_threats(self, threats, current_position):
        """Assess threat levels and provide recommendations"""
        if not threats:
            return {"level": "LOW", "recommendation": "Proceed with standard protocols"}
        
        # Calculate threat proximity and intensity
        total_threat = 0
        closest_threat_distance = float('inf')
        
        for threat in threats:
            if 'position' in threat:
                distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(current_position, threat['position'])))
                intensity = threat.get('intensity', 1.0)
                total_threat += intensity / (distance + 1)
                closest_threat_distance = min(closest_threat_distance, distance)
        
        if total_threat > 2.0:
            level = "CRITICAL"
            recommendation = "Immediate evasive action required. Consider alternate route."
        elif total_threat > 1.0:
            level = "HIGH"
            recommendation = "Increased caution advised. Monitor threat movements."
        elif total_threat > 0.3:
            level = "MEDIUM"
            recommendation = "Maintain alertness. Continue mission with enhanced surveillance."
        else:
            level = "LOW"
            recommendation = "Proceed with standard protocols."
        
        return {
            "level": level,
            "recommendation": recommendation,
            "total_threat_score": float(total_threat),
            "closest_threat_distance": float(closest_threat_distance)
        }
    
    def _estimate_travel_time(self, current_pos, target_pos):
        """Estimate travel time to target"""
        distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(current_pos, target_pos)))
        # Assume average speed of 1 unit per time step
        return {"distance": float(distance), "estimated_time_steps": int(distance)}
    
    def _calculate_risk_level(self, state, threats):
        """Calculate overall mission risk level"""
        terrain_difficulty = np.std(state[0])  # Terrain variance
        threat_density = np.mean(state[3])     # Average threat level
        
        risk_score = 0.4 * terrain_difficulty + 0.6 * threat_density
        
        if risk_score > 0.7:
            return "HIGH"
        elif risk_score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"

# Factory function for creating navigation agents
def create_navigation_agent(config_path=None):
    """Factory function to create and configure navigation agent"""
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            'state_size': (4, 64, 64),  # 4 channels, 64x64 grid
            'action_size': 9,           # 8 directions + wait
            'learning_rate': 1e-4,
            'gamma': 0.99,
            'epsilon': 1.0,
            'epsilon_min': 0.01,
            'epsilon_decay': 0.995,
            'batch_size': 32,
            'update_target_freq': 1000,
            'memory_size': 100000
        }
    
    agent = AutonomousNavigationAgent(
        state_size=config['state_size'],
        action_size=config['action_size'],
        config=config
    )
    
    return agent

# Main execution for testing
if __name__ == "__main__":
    # Create test environment
    terrain = np.random.rand(64, 64) * 100  # Random terrain
    current_pos = (10, 10)
    target_pos = (50, 50)
    threats = [
        {"position": (25, 25), "intensity": 0.8, "type": "enemy_unit"},
        {"position": (30, 35), "intensity": 0.6, "type": "minefield"}
    ]
    
    # Create and test agent
    agent = create_navigation_agent()
    decision = agent.get_navigation_decision(terrain, current_pos, target_pos, threats)
    
    print("Navigation Decision:")
    print(json.dumps(decision, indent=2))
    
    logger.info("Autonomous navigation system test completed successfully")