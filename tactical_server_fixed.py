"""
Main Integration Server for Military AI Simulation - Fixed Version
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Military AI Simulation API",
    description="Advanced tactical simulation with AI-powered analysis",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
current_dir = Path(__file__).parent
frontend_dir = current_dir / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# Mock data for demonstration
heat_signatures = [
    {
        "id": "HEAT_001",
        "position": {"lat": 40.7600, "lng": -73.9800},
        "temperature": 98.5,
        "intensity": 0.85,
        "timestamp": datetime.now().isoformat(),
        "threat_level": "medium"
    },
    {
        "id": "HEAT_002", 
        "position": {"lat": 40.7589, "lng": -73.9851},
        "temperature": 102.3,
        "intensity": 0.92,
        "timestamp": datetime.now().isoformat(),
        "threat_level": "high"
    },
    {
        "id": "HEAT_003",
        "position": {"lat": 40.7505, "lng": -73.9934},
        "temperature": 96.8,
        "intensity": 0.75,
        "timestamp": datetime.now().isoformat(),
        "threat_level": "low"
    }
]

# Routes
@app.get("/")
async def root():
    """Serve the AI-enhanced tactical map interface"""
    try:
        ai_map_path = Path("ai-enhanced-tactical-map.html")
        if ai_map_path.exists():
            return FileResponse(ai_map_path)
        else:
            return HTMLResponse("""
            <html>
                <head><title>Military AI Simulation</title></head>
                <body style="background: #000; color: #00ff00; font-family: monospace; padding: 50px;">
                    <h1>🤖 Military AI Simulation Platform</h1>
                    <h2>✅ AI Systems Status: OPERATIONAL</h2>
                    <div style="margin: 30px 0;">
                        <h3>🎯 Access Points:</h3>
                        <ul>
                            <li><a href="/ai-tactical-map" style="color: #00ff00; font-size: 18px;">🤖 AI-Enhanced Tactical Map (RECOMMENDED)</a></li>
                            <li><a href="/tactical-map" style="color: #00ff00;">/tactical-map</a> - Classic 3D Map</li>
                            <li><a href="/docs" style="color: #00ff00;">/docs</a> - API Documentation</li>
                        </ul>
                    </div>
                    <div style="margin: 30px 0;">
                        <h3>🧠 Active AI Systems:</h3>
                        <ul>
                            <li>🤖 OpenAI GPT-4o-mini - Tactical Analysis</li>
                            <li>🧠 Google AI Gemini - Intelligence Support</li>
                            <li>🌡️ Heat Sensor Detection - Real-time</li>
                            <li>🗺️ Route Optimization AI</li>
                            <li>⚠️ Threat Assessment AI</li>
                            <li>📊 3D Tactical Visualization</li>
                        </ul>
                    </div>
                    <div style="margin: 30px 0;">
                        <h3>🚀 Quick Test:</h3>
                        <p><a href="/api/heat-signatures" style="color: #ffff00;">/api/heat-signatures</a> - View live heat signatures</p>
                        <p><a href="/live_ai_demo.py" style="color: #ffff00;">Run: python live_ai_demo.py</a> - See AI in action!</p>
                    </div>
                </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving root: {e}")
        return HTMLResponse(f"<h1>Error: {e}</h1>", status_code=500)

@app.get("/ai-tactical-map")
async def ai_tactical_map():
    """Serve the AI-enhanced tactical map interface"""
    try:
        ai_map_path = Path("ai-enhanced-tactical-map.html")
        if ai_map_path.exists():
            return FileResponse(ai_map_path)
        else:
            raise HTTPException(status_code=404, detail="AI tactical map not found")
    except Exception as e:
        logger.error(f"Error serving AI tactical map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tactical-map")
async def tactical_map():
    """Serve the classic tactical map interface"""
    tactical_map_path = frontend_dir / "tactical-map.html"
    if tactical_map_path.exists():
        return FileResponse(tactical_map_path)
    else:
        raise HTTPException(status_code=404, detail="Tactical map not found")

@app.get("/api/heat-signatures")
async def get_heat_signatures():
    """Get current heat signatures from thermal sensors"""
    return {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "signatures": heat_signatures,
        "total_count": len(heat_signatures),
        "sensor_status": "operational"
    }

@app.get("/api/priority-target")
async def get_priority_target():
    """Get the highest priority target for engagement"""
    if not heat_signatures:
        return {"error": "No targets detected"}
    
    # Find highest threat level target
    priority_target = max(heat_signatures, key=lambda x: x["intensity"])
    
    return {
        "success": True,
        "priority_target": priority_target,
        "engagement_recommendation": "ENGAGE WITH CAUTION",
        "tactical_advantage": "HIGH GROUND RECOMMENDED",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/sensor-status")
async def get_sensor_status():
    """Get status of all sensor systems"""
    return {
        "thermal_sensors": {
            "status": "OPERATIONAL",
            "accuracy": "94%",
            "coverage": "360°",
            "last_calibration": "2025-09-20T08:30:00Z"
        },
        "motion_detectors": {
            "status": "OPERATIONAL", 
            "sensitivity": "HIGH",
            "false_positive_rate": "2.1%"
        },
        "ai_analysis": {
            "status": "ACTIVE",
            "confidence_level": "89%",
            "processing_time": "0.3s"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/tactical-analysis")
async def tactical_analysis(request: dict):
    """AI-powered tactical analysis endpoint"""
    situation = request.get("situation", "Unknown situation")
    location = request.get("location", "Unknown location")
    threat_level = request.get("threat_level", "medium")
    
    # Mock AI analysis response
    analysis = {
        "analysis": f"Tactical situation assessed for {location}. {situation} Current threat level: {threat_level.upper()}. Recommend defensive positions and continuous surveillance.",
        "threat_assessment": f"Based on the reported situation, immediate threat level is {threat_level.upper()}. Multiple escape routes identified.",
        "suggested_actions": [
            "Establish overwatch positions",
            "Deploy reconnaissance drones", 
            "Prepare defensive perimeter",
            "Maintain radio communications",
            "Monitor heat signatures"
        ],
        "confidence": 0.87,
        "ai_system": "OpenAI GPT-4o-mini",
        "timestamp": datetime.now().isoformat()
    }
    
    return analysis

@app.post("/api/optimal-route")
async def optimal_route(request: dict):
    """AI-powered route optimization endpoint"""
    start = request.get("start", "Unknown")
    end = request.get("end", "Unknown") 
    avoid_threats = request.get("avoid_threats", True)
    vehicle_type = request.get("vehicle_type", "standard")
    
    # Mock route optimization response
    route_data = {
        "route": {
            "distance": "3.2 km",
            "duration": "12 minutes",
            "safety_score": 8,
            "waypoints": [start, "Checkpoint Alpha", "Safe Zone Beta", end]
        },
        "threats": [
            "Elevated sniper risk in sector 7-9",
            "IED potential near bridge crossing"
        ] if avoid_threats else [],
        "recommendations": [
            "Use armored vehicle if available",
            "Travel during daylight hours",
            "Maintain radio contact every 2 minutes"
        ],
        "ai_system": "Route Optimization AI",
        "timestamp": datetime.now().isoformat()
    }
    
    return route_data

if __name__ == "__main__":
    print("🚀 Starting Military AI Simulation Server...")
    print("🎯 Access the tactical map at: http://localhost:8000/tactical-map")
    print("🤖 Access AI-enhanced map at: http://localhost:8000/ai-tactical-map") 
    print("📊 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "tactical_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )