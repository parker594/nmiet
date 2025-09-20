"""
AI Models Manager for Military Simulation
Handles multiple AI model APIs and integrations
"""

import os
import json
import requests
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ModelType(Enum):
    TACTICAL_ANALYSIS = "tactical_analysis"
    THREAT_DETECTION = "threat_detection"
    ROUTE_PLANNING = "route_planning"
    ENEMY_BEHAVIOR = "enemy_behavior"
    WEATHER_ANALYSIS = "weather_analysis"
    TERRAIN_ANALYSIS = "terrain_analysis"

@dataclass
class AIModelConfig:
    name: str
    api_key: str
    endpoint: str
    model_type: ModelType
    parameters: Dict[str, Any]

class AIModelsManager:
    def __init__(self):
        self.models = {}
        self.load_model_configurations()
    
    def load_model_configurations(self):
        """Load AI model configurations from environment variables"""
        
        # OpenAI Models
        if os.getenv('OPENAI_API_KEY'):
            self.models['openai_tactical'] = AIModelConfig(
                name="OpenAI GPT-4 Tactical",
                api_key=os.getenv('OPENAI_API_KEY'),
                endpoint="https://api.openai.com/v1/chat/completions",
                model_type=ModelType.TACTICAL_ANALYSIS,
                parameters={
                    "model": os.getenv('OPENAI_MODEL', 'gpt-4'),
                    "temperature": 0.3,
                    "max_tokens": 1000
                }
            )
        
        # Google AI Models
        if os.getenv('GOOGLE_AI_API_KEY'):
            self.models['google_ai'] = AIModelConfig(
                name="Google AI Gemini",
                api_key=os.getenv('GOOGLE_AI_API_KEY'),
                endpoint="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent",
                model_type=ModelType.ENEMY_BEHAVIOR,
                parameters={
                    "temperature": 0.4,
                    "maxOutputTokens": 1000
                }
            )
        
        # Hugging Face Models
        if os.getenv('HUGGINGFACE_API_KEY'):
            self.models['huggingface_threat'] = AIModelConfig(
                name="Hugging Face Threat Detection",
                api_key=os.getenv('HUGGINGFACE_API_KEY'),
                endpoint=f"{os.getenv('HUGGINGFACE_MODEL_ENDPOINT')}microsoft/DialoGPT-large",
                model_type=ModelType.THREAT_DETECTION,
                parameters={
                    "temperature": 0.2,
                    "max_length": 500
                }
            )
        
        # Azure Cognitive Services
        if os.getenv('AZURE_COGNITIVE_SERVICES_KEY'):
            self.models['azure_cognitive'] = AIModelConfig(
                name="Azure Cognitive Services",
                api_key=os.getenv('AZURE_COGNITIVE_SERVICES_KEY'),
                endpoint=os.getenv('AZURE_COGNITIVE_ENDPOINT'),
                model_type=ModelType.TERRAIN_ANALYSIS,
                parameters={
                    "language": "en",
                    "confidence_threshold": 0.8
                }
            )
        
        logger.info(f"Loaded {len(self.models)} AI model configurations")
    
    async def get_tactical_analysis(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Get tactical analysis for a given situation"""
        try:
            model = self.models.get('openai_tactical')
            if not model:
                return self._get_mock_tactical_analysis(situation)
            
            prompt = f"""
            Military Tactical Analysis Request:
            
            Situation:
            - Enemy Position: {situation.get('enemy_position', 'Unknown')}
            - Friendly Forces: {situation.get('friendly_forces', 'Unknown')}
            - Terrain: {situation.get('terrain', 'Unknown')}
            - Weather: {situation.get('weather', 'Clear')}
            - Mission Objective: {situation.get('objective', 'Neutralize threat')}
            
            Provide tactical recommendations including:
            1. Best approach routes
            2. Recommended tactics
            3. Risk assessment
            4. Resource requirements
            5. Timeline estimation
            
            Format as JSON with clear recommendations.
            """
            
            headers = {
                "Authorization": f"Bearer {model.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model.parameters["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": model.parameters["temperature"],
                "max_tokens": model.parameters["max_tokens"]
            }
            
            response = requests.post(model.endpoint, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                return {
                    "analysis": content,
                    "model_used": model.name,
                    "confidence": 0.85,
                    "timestamp": json.dumps({"$date": {"$numberLong": str(int(os.times().elapsed * 1000))}})
                }
            else:
                logger.warning(f"OpenAI API error: {response.status_code}")
                return self._get_mock_tactical_analysis(situation)
                
        except Exception as e:
            logger.error(f"Error in tactical analysis: {e}")
            return self._get_mock_tactical_analysis(situation)
    
    async def get_enemy_behavior_prediction(self, enemy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict enemy behavior patterns"""
        try:
            # Use multiple models for comprehensive analysis
            predictions = []
            
            # Analyze movement patterns
            movement_analysis = self._analyze_movement_patterns(enemy_data)
            predictions.append(movement_analysis)
            
            # Analyze tactical patterns
            tactical_analysis = self._analyze_tactical_patterns(enemy_data)
            predictions.append(tactical_analysis)
            
            return {
                "predictions": predictions,
                "confidence": 0.78,
                "next_likely_actions": [
                    "Defensive positioning",
                    "Flanking maneuver",
                    "Retreat to secondary position"
                ],
                "threat_level": self._calculate_threat_level(enemy_data)
            }
            
        except Exception as e:
            logger.error(f"Error in enemy behavior prediction: {e}")
            return {"error": "Analysis failed", "fallback": True}
    
    async def get_optimal_route(self, start: tuple, end: tuple, constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal route considering tactical constraints"""
        try:
            # Mock route calculation with tactical considerations
            route_data = {
                "waypoints": [
                    {"lat": start[0], "lng": start[1], "type": "start"},
                    {"lat": (start[0] + end[0]) / 2, "lng": (start[1] + end[1]) / 2, "type": "tactical_waypoint"},
                    {"lat": end[0], "lng": end[1], "type": "destination"}
                ],
                "distance_km": self._calculate_distance(start, end),
                "estimated_time_minutes": 45,
                "risk_assessment": {
                    "overall_risk": "MEDIUM",
                    "threat_zones": [
                        {"position": [start[0] + 0.001, start[1] + 0.001], "radius": 500, "type": "sniper"}
                    ]
                },
                "tactical_recommendations": [
                    "Use smoke cover at waypoint 2",
                    "Maintain radio silence in threat zones",
                    "Prepare for possible contact at destination"
                ]
            }
            
            return route_data
            
        except Exception as e:
            logger.error(f"Error in route planning: {e}")
            return {"error": "Route calculation failed"}
    
    def _get_mock_tactical_analysis(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """Mock tactical analysis when API is unavailable"""
        return {
            "analysis": {
                "approach_routes": [
                    {"route": "North approach", "risk": "LOW", "time": "15 minutes"},
                    {"route": "East flanking", "risk": "MEDIUM", "time": "25 minutes"},
                    {"route": "South indirect", "risk": "LOW", "time": "35 minutes"}
                ],
                "recommended_tactics": [
                    "Use suppressive fire to pin enemy",
                    "Coordinate simultaneous assault from multiple angles",
                    "Maintain communication with support elements"
                ],
                "risk_assessment": {
                    "overall_risk": "MEDIUM",
                    "casualty_estimate": "1-2 personnel",
                    "mission_success_probability": "85%"
                },
                "resource_requirements": {
                    "personnel": "8-12 soldiers",
                    "equipment": ["Body armor", "Communication gear", "Smoke grenades"],
                    "support": "Artillery on standby"
                },
                "timeline": {
                    "preparation": "10 minutes",
                    "approach": "15-35 minutes",
                    "engagement": "5-15 minutes",
                    "consolidation": "10 minutes"
                }
            },
            "model_used": "Mock Tactical AI",
            "confidence": 0.75,
            "fallback": True
        }
    
    def _analyze_movement_patterns(self, enemy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze enemy movement patterns"""
        return {
            "pattern_type": "Defensive positioning",
            "predictability": 0.7,
            "next_move_probability": {
                "stay_position": 0.4,
                "retreat": 0.3,
                "advance": 0.2,
                "flank": 0.1
            }
        }
    
    def _analyze_tactical_patterns(self, enemy_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze enemy tactical patterns"""
        return {
            "tactics_observed": ["Defensive", "Use of cover"],
            "equipment_detected": ["Rifles", "Communication equipment"],
            "skill_level": "INTERMEDIATE",
            "coordination_level": "GOOD"
        }
    
    def _calculate_threat_level(self, enemy_data: Dict[str, Any]) -> str:
        """Calculate overall threat level"""
        personnel = enemy_data.get('personnel_count', 1)
        equipment = len(enemy_data.get('equipment', []))
        position_strength = enemy_data.get('position_strength', 0.5)
        
        threat_score = (personnel * 0.4) + (equipment * 0.3) + (position_strength * 0.3)
        
        if threat_score > 0.7:
            return "HIGH"
        elif threat_score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_distance(self, start: tuple, end: tuple) -> float:
        """Calculate distance between two points (simplified)"""
        import math
        lat1, lon1 = start
        lat2, lon2 = end
        
        # Simplified distance calculation
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        distance = math.sqrt(dlat**2 + dlon**2) * 111  # Rough km conversion
        
        return round(distance, 2)

# Global instance
ai_models_manager = AIModelsManager()