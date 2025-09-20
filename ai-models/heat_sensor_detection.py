"""
Heat Sensor Detection System for Military AI Simulation
Simulates thermal imaging and heat signature detection
"""

import os
import numpy as np
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import random
import math

logger = logging.getLogger(__name__)

@dataclass
class HeatSignature:
    """Represents a detected heat signature"""
    id: str
    position: Tuple[float, float]  # lat, lng
    temperature: float
    intensity: float
    size: float  # in meters
    confidence: float
    timestamp: datetime
    signature_type: str  # 'vehicle', 'personnel', 'equipment', 'unknown'
    threat_level: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'

@dataclass
class ThermalSensor:
    """Represents a thermal sensor with its properties"""
    id: str
    position: Tuple[float, float]
    range_km: float
    resolution: float
    accuracy: float
    status: str  # 'active', 'inactive', 'maintenance'

class HeatSensorSystem:
    """Advanced Heat Sensor Detection System"""
    
    def __init__(self):
        self.sensors = []
        self.detected_signatures = []
        self.heat_threshold = float(os.getenv('HEAT_SENSOR_THRESHOLD', 85.0))
        self.detection_radius = float(os.getenv('HEAT_DETECTION_RADIUS', 500))
        self.army_base_coords = self._parse_coordinates(os.getenv('ARMY_BASE_COORDINATES', '40.7589,-73.9851'))
        
        # Initialize thermal sensors around the area
        self._initialize_sensors()
        
        # Generate some hardcoded heat signatures for demo
        self._generate_demo_heat_signatures()
        
        logger.info(f"Heat Sensor System initialized with {len(self.sensors)} sensors")
    
    def _parse_coordinates(self, coord_string: str) -> Tuple[float, float]:
        """Parse coordinate string to tuple"""
        try:
            lat, lng = map(float, coord_string.split(','))
            return (lat, lng)
        except:
            return (40.7589, -73.9851)  # Default NYC coordinates
    
    def _initialize_sensors(self):
        """Initialize thermal sensors around the operational area"""
        base_lat, base_lng = self.army_base_coords
        
        # Create a grid of sensors around the base
        sensor_positions = [
            (base_lat + 0.01, base_lng + 0.01),   # Northeast
            (base_lat + 0.01, base_lng - 0.01),   # Northwest
            (base_lat - 0.01, base_lng + 0.01),   # Southeast
            (base_lat - 0.01, base_lng - 0.01),   # Southwest
            (base_lat, base_lng + 0.015),         # East
            (base_lat, base_lng - 0.015),         # West
            (base_lat + 0.015, base_lng),         # North
            (base_lat - 0.015, base_lng),         # South
        ]
        
        for i, position in enumerate(sensor_positions):
            sensor = ThermalSensor(
                id=f"THERMAL_SENSOR_{i+1:02d}",
                position=position,
                range_km=2.5,
                resolution=0.1,  # degrees Celsius
                accuracy=0.95,
                status='active'
            )
            self.sensors.append(sensor)
    
    def _generate_demo_heat_signatures(self):
        """Generate hardcoded heat signatures for demonstration"""
        base_lat, base_lng = self.army_base_coords
        
        # Enemy positions with different threat levels
        demo_signatures = [
            {
                "position": (base_lat + 0.008, base_lng + 0.012),
                "temperature": 98.5,
                "intensity": 0.9,
                "size": 15.0,
                "signature_type": "vehicle",
                "threat_level": "HIGH",
                "description": "Enemy tank detected"
            },
            {
                "position": (base_lat + 0.005, base_lng - 0.008),
                "temperature": 92.3,
                "intensity": 0.7,
                "size": 8.0,
                "signature_type": "personnel",
                "threat_level": "MEDIUM",
                "description": "Enemy patrol (4-6 personnel)"
            },
            {
                "position": (base_lat - 0.006, base_lng + 0.009),
                "temperature": 105.2,
                "intensity": 0.95,
                "size": 25.0,
                "signature_type": "equipment",
                "threat_level": "CRITICAL",
                "description": "Enemy artillery position"
            },
            {
                "position": (base_lat + 0.003, base_lng + 0.004),
                "temperature": 88.7,
                "intensity": 0.5,
                "size": 5.0,
                "signature_type": "personnel",
                "threat_level": "LOW",
                "description": "Single enemy operative"
            },
            {
                "position": (base_lat - 0.004, base_lng - 0.011),
                "temperature": 95.8,
                "intensity": 0.8,
                "size": 18.0,
                "signature_type": "vehicle",
                "threat_level": "HIGH",
                "description": "Enemy APC with personnel"
            }
        ]
        
        for i, sig_data in enumerate(demo_signatures):
            signature = HeatSignature(
                id=f"HEAT_SIG_{i+1:03d}",
                position=sig_data["position"],
                temperature=sig_data["temperature"],
                intensity=sig_data["intensity"],
                size=sig_data["size"],
                confidence=0.85 + random.uniform(0, 0.15),
                timestamp=datetime.now(),
                signature_type=sig_data["signature_type"],
                threat_level=sig_data["threat_level"]
            )
            self.detected_signatures.append(signature)
    
    def scan_for_heat_signatures(self) -> List[Dict[str, Any]]:
        """Perform a scan for heat signatures"""
        current_time = datetime.now()
        
        # Add some random noise and variation to existing signatures
        for signature in self.detected_signatures:
            # Slightly vary temperature and position to simulate movement
            signature.temperature += random.uniform(-2, 2)
            signature.position = (
                signature.position[0] + random.uniform(-0.0001, 0.0001),
                signature.position[1] + random.uniform(-0.0001, 0.0001)
            )
            signature.timestamp = current_time
        
        # Occasionally add new signatures
        if random.random() < 0.3:  # 30% chance
            self._add_random_signature()
        
        # Remove signatures that have "moved away" (simulate dynamic environment)
        self.detected_signatures = [sig for sig in self.detected_signatures if random.random() > 0.05]
        
        # Convert to dictionary format for API response
        signatures_data = []
        for signature in self.detected_signatures:
            signatures_data.append({
                "id": signature.id,
                "position": {
                    "lat": signature.position[0],
                    "lng": signature.position[1]
                },
                "temperature": round(signature.temperature, 1),
                "intensity": round(signature.intensity, 2),
                "size_meters": round(signature.size, 1),
                "confidence": round(signature.confidence, 2),
                "timestamp": signature.timestamp.isoformat(),
                "type": signature.signature_type,
                "threat_level": signature.threat_level,
                "distance_from_base": self._calculate_distance_from_base(signature.position),
                "recommended_action": self._get_recommended_action(signature)
            })
        
        return signatures_data
    
    def _add_random_signature(self):
        """Add a random heat signature to simulate new detections"""
        base_lat, base_lng = self.army_base_coords
        
        # Generate random position within sensor range
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0.002, 0.015)  # Random distance from base
        
        new_position = (
            base_lat + distance * math.cos(angle),
            base_lng + distance * math.sin(angle)
        )
        
        signature_types = ['vehicle', 'personnel', 'equipment', 'unknown']
        threat_levels = ['LOW', 'MEDIUM', 'HIGH']
        
        new_signature = HeatSignature(
            id=f"HEAT_SIG_{len(self.detected_signatures)+1:03d}",
            position=new_position,
            temperature=random.uniform(85, 110),
            intensity=random.uniform(0.3, 1.0),
            size=random.uniform(3, 30),
            confidence=random.uniform(0.6, 0.95),
            timestamp=datetime.now(),
            signature_type=random.choice(signature_types),
            threat_level=random.choice(threat_levels)
        )
        
        self.detected_signatures.append(new_signature)
    
    def _calculate_distance_from_base(self, position: Tuple[float, float]) -> float:
        """Calculate distance from army base"""
        base_lat, base_lng = self.army_base_coords
        lat, lng = position
        
        # Simplified distance calculation
        dlat = lat - base_lat
        dlng = lng - base_lng
        distance_km = math.sqrt(dlat**2 + dlng**2) * 111  # Rough conversion to km
        
        return round(distance_km, 2)
    
    def _get_recommended_action(self, signature: HeatSignature) -> str:
        """Get recommended action based on heat signature"""
        if signature.threat_level == "CRITICAL":
            return "IMMEDIATE RESPONSE - Deploy heavy assets"
        elif signature.threat_level == "HIGH":
            return "HIGH PRIORITY - Dispatch assault team"
        elif signature.threat_level == "MEDIUM":
            return "MEDIUM PRIORITY - Send reconnaissance unit"
        else:
            return "LOW PRIORITY - Monitor and track"
    
    def get_highest_priority_target(self) -> Dict[str, Any]:
        """Get the highest priority target for tactical response"""
        if not self.detected_signatures:
            return {"message": "No targets detected"}
        
        # Sort by threat level and proximity to base
        priority_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        
        highest_priority = max(
            self.detected_signatures,
            key=lambda sig: (
                priority_order.get(sig.threat_level, 0),
                -self._calculate_distance_from_base(sig.position)  # Closer is higher priority
            )
        )
        
        return {
            "target_id": highest_priority.id,
            "position": {
                "lat": highest_priority.position[0],
                "lng": highest_priority.position[1]
            },
            "threat_level": highest_priority.threat_level,
            "type": highest_priority.signature_type,
            "distance_km": self._calculate_distance_from_base(highest_priority.position),
            "recommended_response": self._get_tactical_response(highest_priority)
        }
    
    def _get_tactical_response(self, signature: HeatSignature) -> Dict[str, Any]:
        """Get detailed tactical response recommendation"""
        base_position = self.army_base_coords
        target_position = signature.position
        
        return {
            "approach_route": self._calculate_optimal_approach(base_position, target_position),
            "recommended_assets": self._get_recommended_assets(signature),
            "estimated_engagement_time": self._estimate_engagement_time(signature),
            "tactical_advice": self._get_tactical_advice(signature),
            "risk_assessment": self._assess_mission_risk(signature)
        }
    
    def _calculate_optimal_approach(self, start: Tuple[float, float], target: Tuple[float, float]) -> List[Dict[str, Any]]:
        """Calculate optimal approach route"""
        # Generate waypoints for tactical approach
        waypoints = []
        
        # Start point (army base)
        waypoints.append({
            "lat": start[0],
            "lng": start[1],
            "type": "departure",
            "description": "Army base - mission start"
        })
        
        # Tactical waypoint (approach from cover)
        mid_lat = (start[0] + target[0]) / 2
        mid_lng = (start[1] + target[1]) / 2
        
        # Add offset for tactical approach
        waypoints.append({
            "lat": mid_lat + 0.001,
            "lng": mid_lng - 0.001,
            "type": "tactical_position",
            "description": "Overwatch position - establish reconnaissance"
        })
        
        # Final assault position
        waypoints.append({
            "lat": target[0] - 0.0005,
            "lng": target[1] - 0.0005,
            "type": "assault_position",
            "description": "Final assault position"
        })
        
        # Target
        waypoints.append({
            "lat": target[0],
            "lng": target[1],
            "type": "target",
            "description": "Enemy position - engage"
        })
        
        return waypoints
    
    def _get_recommended_assets(self, signature: HeatSignature) -> List[str]:
        """Get recommended military assets for engagement"""
        if signature.threat_level == "CRITICAL":
            return ["Heavy armor", "Artillery support", "Air support", "Special forces"]
        elif signature.threat_level == "HIGH":
            return ["Armored vehicles", "Infantry squad", "Sniper support"]
        elif signature.threat_level == "MEDIUM":
            return ["Infantry team", "Light vehicles", "Reconnaissance drone"]
        else:
            return ["Reconnaissance team", "Light weapons"]
    
    def _estimate_engagement_time(self, signature: HeatSignature) -> Dict[str, int]:
        """Estimate time for different phases of engagement"""
        distance = self._calculate_distance_from_base(signature.position)
        
        return {
            "preparation_minutes": 5 + (2 if signature.threat_level in ["HIGH", "CRITICAL"] else 0),
            "travel_minutes": int(distance * 3),  # 3 minutes per km (tactical movement)
            "engagement_minutes": 10 + (5 if signature.threat_level == "CRITICAL" else 0),
            "total_minutes": int(distance * 3) + 15 + (7 if signature.threat_level in ["HIGH", "CRITICAL"] else 0)
        }
    
    def _get_tactical_advice(self, signature: HeatSignature) -> List[str]:
        """Get tactical advice for engagement"""
        advice = []
        
        if signature.signature_type == "vehicle":
            advice.extend([
                "Use anti-tank weapons",
                "Approach from flanks to avoid frontal armor",
                "Coordinate simultaneous assault"
            ])
        elif signature.signature_type == "personnel":
            advice.extend([
                "Use suppressive fire",
                "Employ smoke for concealment",
                "Coordinate team movements"
            ])
        elif signature.signature_type == "equipment":
            advice.extend([
                "Priority target - eliminate quickly",
                "Use precision strikes",
                "Prevent enemy from using equipment"
            ])
        
        if signature.threat_level in ["HIGH", "CRITICAL"]:
            advice.append("Request immediate backup")
            advice.append("Establish communications with command")
        
        return advice
    
    def _assess_mission_risk(self, signature: HeatSignature) -> Dict[str, Any]:
        """Assess mission risk factors"""
        risk_factors = []
        overall_risk = "LOW"
        
        if signature.threat_level in ["HIGH", "CRITICAL"]:
            risk_factors.append("High threat target")
            overall_risk = "HIGH"
        
        distance = self._calculate_distance_from_base(signature.position)
        if distance > 5:
            risk_factors.append("Long distance from base")
            overall_risk = "MEDIUM" if overall_risk == "LOW" else overall_risk
        
        if signature.signature_type == "vehicle":
            risk_factors.append("Armored target")
        
        return {
            "overall_risk": overall_risk,
            "risk_factors": risk_factors,
            "casualty_estimate": "1-3 personnel" if overall_risk == "HIGH" else "0-1 personnel",
            "mission_success_probability": "85%" if overall_risk == "LOW" else "70%"
        }
    
    def get_sensor_status(self) -> Dict[str, Any]:
        """Get status of all thermal sensors"""
        active_sensors = [s for s in self.sensors if s.status == 'active']
        
        return {
            "total_sensors": len(self.sensors),
            "active_sensors": len(active_sensors),
            "coverage_area_km2": len(active_sensors) * 19.6,  # ~2.5km radius each
            "detection_range_km": 2.5,
            "current_detections": len(self.detected_signatures),
            "sensors": [
                {
                    "id": sensor.id,
                    "position": {"lat": sensor.position[0], "lng": sensor.position[1]},
                    "status": sensor.status,
                    "range_km": sensor.range_km,
                    "accuracy": sensor.accuracy
                }
                for sensor in self.sensors
            ]
        }

# Global instance
heat_sensor_system = HeatSensorSystem()