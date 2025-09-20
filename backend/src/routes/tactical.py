"""
Enhanced API routes for Heat Sensor Detection and Tactical Analysis
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime

# Import our AI systems
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai-models'))

try:
    from heat_sensor_detection import heat_sensor_system
    from ai_models_manager import ai_models_manager
except ImportError:
    # Mock systems for development
    class MockHeatSensorSystem:
        def scan_for_heat_signatures(self):
            return [
                {
                    "id": "HEAT_001",
                    "position": {"lat": 40.7600, "lng": -73.9800},
                    "temperature": 98.5,
                    "threat_level": "HIGH",
                    "type": "vehicle",
                    "distance_from_base": 1.2
                }
            ]
        
        def get_highest_priority_target(self):
            return {
                "target_id": "HEAT_001",
                "threat_level": "HIGH",
                "recommended_response": {
                    "approach_route": [],
                    "recommended_assets": ["Infantry", "Support"],
                    "tactical_advice": ["Use cover", "Coordinate assault"]
                }
            }
    
    class MockAIModelsManager:
        async def get_tactical_analysis(self, situation):
            return {
                "analysis": "Mock tactical analysis",
                "confidence": 0.85
            }
        
        async def get_optimal_route(self, start, end, constraints):
            return {
                "waypoints": [
                    {"lat": start[0], "lng": start[1], "type": "start"},
                    {"lat": end[0], "lng": end[1], "type": "destination"}
                ]
            }
    
    heat_sensor_system = MockHeatSensorSystem()
    ai_models_manager = MockAIModelsManager()

router = APIRouter()

@router.get("/heat-signatures")
async def get_heat_signatures():
    """Get current heat signatures from thermal sensors"""
    try:
        signatures = heat_sensor_system.scan_for_heat_signatures()
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "signatures": signatures,
            "total_count": len(signatures),
            "sensor_status": "operational"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scanning heat signatures: {str(e)}")

@router.get("/priority-target")
async def get_priority_target():
    """Get the highest priority target for engagement"""
    try:
        target = heat_sensor_system.get_highest_priority_target()
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "priority_target": target
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting priority target: {str(e)}")

@router.post("/tactical-analysis")
async def request_tactical_analysis(situation: Dict[str, Any]):
    """Request AI tactical analysis for current situation"""
    try:
        # Get tactical analysis from AI models
        analysis = await ai_models_manager.get_tactical_analysis(situation)
        
        # Get enemy behavior prediction if enemies are present
        enemy_prediction = None
        if "heat_signatures" in situation:
            enemy_data = {
                "positions": [sig.get("position") for sig in situation["heat_signatures"]],
                "personnel_count": len(situation["heat_signatures"]),
                "equipment": [sig.get("type") for sig in situation["heat_signatures"]]
            }
            enemy_prediction = await ai_models_manager.get_enemy_behavior_prediction(enemy_data)
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "tactical_analysis": analysis,
            "enemy_prediction": enemy_prediction,
            "recommendations": generate_tactical_recommendations(situation, analysis)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in tactical analysis: {str(e)}")

@router.post("/optimal-route")
async def calculate_optimal_route(route_request: Dict[str, Any]):
    """Calculate optimal route from base to target"""
    try:
        start = route_request.get("start", [40.7589, -73.9851])  # Army base
        end = route_request.get("end")
        constraints = route_request.get("constraints", {})
        
        if not end:
            raise HTTPException(status_code=400, detail="End coordinates required")
        
        # Get optimal route from AI
        route = await ai_models_manager.get_optimal_route(tuple(start), tuple(end), constraints)
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "route": route,
            "mission_brief": generate_mission_brief(start, end, route)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating route: {str(e)}")

@router.post("/deploy-assets")
async def deploy_military_assets(deployment_request: Dict[str, Any]):
    """Deploy military assets to target location"""
    try:
        target_id = deployment_request.get("target_id")
        asset_types = deployment_request.get("assets", [])
        
        if not target_id:
            raise HTTPException(status_code=400, detail="Target ID required")
        
        # Simulate asset deployment
        deployment_result = {
            "deployment_id": f"DEPLOY_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "target_id": target_id,
            "assets_deployed": asset_types or ["Infantry Squad", "Support Vehicle"],
            "estimated_arrival": "15 minutes",
            "mission_status": "EN_ROUTE",
            "deployment_time": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "deployment": deployment_result,
            "tracking_info": {
                "real_time_updates": True,
                "communication_channel": "SECURE_CHANNEL_1",
                "emergency_recall": "Available"
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying assets: {str(e)}")

@router.get("/sensor-status")
async def get_sensor_status():
    """Get status of all thermal sensors"""
    try:
        if hasattr(heat_sensor_system, 'get_sensor_status'):
            status = heat_sensor_system.get_sensor_status()
        else:
            # Mock sensor status
            status = {
                "total_sensors": 8,
                "active_sensors": 8,
                "coverage_area_km2": 157,
                "detection_range_km": 2.5,
                "current_detections": 5
            }
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "sensor_status": status
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sensor status: {str(e)}")

@router.post("/enemy-engagement")
async def plan_enemy_engagement(engagement_request: Dict[str, Any]):
    """Plan tactical engagement with detected enemy"""
    try:
        enemy_position = engagement_request.get("enemy_position")
        enemy_type = engagement_request.get("enemy_type", "unknown")
        threat_level = engagement_request.get("threat_level", "MEDIUM")
        
        if not enemy_position:
            raise HTTPException(status_code=400, detail="Enemy position required")
        
        # Generate engagement plan
        engagement_plan = {
            "engagement_id": f"ENG_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "target_analysis": {
                "position": enemy_position,
                "type": enemy_type,
                "threat_level": threat_level,
                "estimated_personnel": get_estimated_personnel(enemy_type),
                "equipment_assessment": get_equipment_assessment(enemy_type)
            },
            "tactical_plan": {
                "approach_strategy": get_approach_strategy(threat_level),
                "recommended_assets": get_recommended_assets(threat_level, enemy_type),
                "engagement_tactics": get_engagement_tactics(enemy_type),
                "contingency_plans": get_contingency_plans(threat_level)
            },
            "mission_timeline": {
                "preparation": "10 minutes",
                "approach": "15 minutes",
                "engagement": "10-20 minutes",
                "consolidation": "15 minutes",
                "total_estimated": "50-60 minutes"
            },
            "risk_assessment": {
                "mission_risk": get_mission_risk(threat_level),
                "casualty_estimate": get_casualty_estimate(threat_level),
                "success_probability": get_success_probability(threat_level, enemy_type)
            }
        }
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "engagement_plan": engagement_plan
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error planning engagement: {str(e)}")

def generate_tactical_recommendations(situation: Dict[str, Any], analysis: Dict[str, Any]) -> List[str]:
    """Generate tactical recommendations based on situation and AI analysis"""
    recommendations = []
    
    # Analyze threat level
    threat_level = situation.get("threat_level", "LOW")
    heat_signatures = situation.get("heat_signatures", [])
    
    if threat_level == "HIGH":
        recommendations.extend([
            "Deploy heavy assault team immediately",
            "Request air support on standby",
            "Establish perimeter security",
            "Prepare medical evacuation route"
        ])
    elif threat_level == "MEDIUM":
        recommendations.extend([
            "Send reconnaissance team for assessment",
            "Prepare quick reaction force",
            "Monitor enemy movements closely",
            "Establish communication with nearby units"
        ])
    else:
        recommendations.extend([
            "Continue surveillance operations",
            "Maintain current defensive positions",
            "Regular status updates every 15 minutes"
        ])
    
    # Add specific recommendations based on enemy types
    enemy_types = [sig.get("type") for sig in heat_signatures]
    if "vehicle" in enemy_types:
        recommendations.append("Deploy anti-tank capabilities")
    if "personnel" in enemy_types:
        recommendations.append("Use suppressive fire tactics")
    if "equipment" in enemy_types:
        recommendations.append("Priority target - neutralize equipment first")
    
    return recommendations

def generate_mission_brief(start: List[float], end: List[float], route: Dict[str, Any]) -> Dict[str, Any]:
    """Generate mission brief for route execution"""
    return {
        "mission_name": f"ROUTE_EXEC_{datetime.now().strftime('%H%M')}",
        "objective": "Navigate to target location and assess situation",
        "start_coordinates": {"lat": start[0], "lng": start[1]},
        "end_coordinates": {"lat": end[0], "lng": end[1]},
        "waypoint_count": len(route.get("waypoints", [])),
        "estimated_duration": route.get("estimated_time_minutes", "Unknown"),
        "risk_level": route.get("risk_assessment", {}).get("overall_risk", "MEDIUM"),
        "special_instructions": [
            "Maintain radio contact every 5 minutes",
            "Report any deviation from planned route",
            "Use tactical formation during movement"
        ]
    }

def get_estimated_personnel(enemy_type: str) -> str:
    """Estimate enemy personnel based on type"""
    personnel_map = {
        "vehicle": "2-4 personnel",
        "personnel": "1-6 individuals",
        "equipment": "1-3 operators",
        "unknown": "Unknown count"
    }
    return personnel_map.get(enemy_type, "Unknown count")

def get_equipment_assessment(enemy_type: str) -> List[str]:
    """Assess likely enemy equipment"""
    equipment_map = {
        "vehicle": ["Armored vehicle", "Small arms", "Communication equipment"],
        "personnel": ["Small arms", "Personal equipment", "Communication devices"],
        "equipment": ["Heavy weapons", "Electronic equipment", "Support gear"],
        "unknown": ["Unassessed equipment"]
    }
    return equipment_map.get(enemy_type, ["Unassessed equipment"])

def get_approach_strategy(threat_level: str) -> str:
    """Get approach strategy based on threat level"""
    strategies = {
        "LOW": "Direct approach with standard precautions",
        "MEDIUM": "Cautious approach with overwatch support",
        "HIGH": "Indirect approach with multiple teams",
        "CRITICAL": "Full tactical assault with all available assets"
    }
    return strategies.get(threat_level, "Standard tactical approach")

def get_recommended_assets(threat_level: str, enemy_type: str) -> List[str]:
    """Get recommended military assets"""
    base_assets = ["Infantry Squad", "Communication Support"]
    
    if threat_level in ["HIGH", "CRITICAL"]:
        base_assets.extend(["Heavy Weapons Team", "Medical Support", "Command Element"])
    
    if enemy_type == "vehicle":
        base_assets.append("Anti-Tank Team")
    elif enemy_type == "equipment":
        base_assets.append("Explosives Specialist")
    
    return base_assets

def get_engagement_tactics(enemy_type: str) -> List[str]:
    """Get engagement tactics based on enemy type"""
    tactics_map = {
        "vehicle": [
            "Disable mobility first",
            "Attack from flanks to avoid frontal armor",
            "Use cover and concealment"
        ],
        "personnel": [
            "Use suppressive fire",
            "Coordinate team movements",
            "Establish fields of fire"
        ],
        "equipment": [
            "Neutralize equipment before personnel",
            "Use precision targeting",
            "Prevent enemy equipment usage"
        ]
    }
    return tactics_map.get(enemy_type, ["Standard engagement procedures"])

def get_contingency_plans(threat_level: str) -> List[str]:
    """Get contingency plans based on threat level"""
    plans = ["Establish rally point", "Plan withdrawal route"]
    
    if threat_level in ["HIGH", "CRITICAL"]:
        plans.extend([
            "Request immediate reinforcements",
            "Prepare medical evacuation",
            "Establish alternate communication"
        ])
    
    return plans

def get_mission_risk(threat_level: str) -> str:
    """Assess mission risk"""
    risk_map = {
        "LOW": "LOW",
        "MEDIUM": "MEDIUM", 
        "HIGH": "HIGH",
        "CRITICAL": "EXTREME"
    }
    return risk_map.get(threat_level, "MEDIUM")

def get_casualty_estimate(threat_level: str) -> str:
    """Estimate potential casualties"""
    casualty_map = {
        "LOW": "0-1 casualties expected",
        "MEDIUM": "1-2 casualties possible",
        "HIGH": "2-4 casualties likely",
        "CRITICAL": "4+ casualties probable"
    }
    return casualty_map.get(threat_level, "1-2 casualties possible")

def get_success_probability(threat_level: str, enemy_type: str) -> str:
    """Calculate mission success probability"""
    base_success = {
        "LOW": 95,
        "MEDIUM": 85,
        "HIGH": 75,
        "CRITICAL": 65
    }
    
    success_rate = base_success.get(threat_level, 80)
    
    # Adjust based on enemy type
    if enemy_type == "vehicle":
        success_rate -= 5
    elif enemy_type == "equipment":
        success_rate -= 10
    
    return f"{max(50, success_rate)}%"