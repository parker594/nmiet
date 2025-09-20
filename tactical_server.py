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
    """Serve the clean military homepage"""
    try:
        homepage_path = Path("military-homepage.html")
        if homepage_path.exists():
            return FileResponse(homepage_path)
        else:
            return HTMLResponse("""
            <html>
                <head><title>Military AI Command Center</title></head>
                <body style="background: #000; color: #00ff00; font-family: monospace; padding: 50px;">
                    <h1>🎖️ Military AI Command Center</h1>
                    <h2>✅ System Status: OPERATIONAL</h2>
                    <div style="margin: 30px 0;">
                        <h3>🎯 Available Mission Modules:</h3>
                        <ul>
                            <li><a href="/3d-heat-map" style="color: #00ff00; font-size: 18px;">�️ 3D Heat Visualization</a></li>
                            <li><a href="/advanced-military-map" style="color: #00ff00;">🗺️ Tactical Operations Map</a></li>
                            <li><a href="/ai-command-interface" style="color: #00ff00;">🤖 AI Command Interface</a></li>
                            <li><a href="/docs" style="color: #00ff00;">/docs</a> - API Documentation</li>
                        </ul>
                    </div>
                    <div style="margin: 30px 0;">
                        <h3>🧠 AI Systems Status:</h3>
                        <ul>
                            <li>🤖 OpenAI GPT-4o-mini - READY</li>
                            <li>🧠 Google AI Gemini - READY</li>
                            <li>🌡️ 3D Heat Mapping - ACTIVE</li>
                            <li>🗺️ Tactical Maps - OPERATIONAL</li>
                            <li>🚁 Drone Systems - STANDBY</li>
                        </ul>
                    </div>
                </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving root: {e}")
        return HTMLResponse(f"<h1>Error: {e}</h1>", status_code=500)

@app.get("/3d-heat-map")
async def heat_map_3d():
    """Serve the 3D heat visualization"""
    try:
        heat_map_path = Path("3d-heat-map.html")
        if heat_map_path.exists():
            return FileResponse(heat_map_path)
        else:
            raise HTTPException(status_code=404, detail="3D heat map not found")
    except Exception as e:
        logger.error(f"Error serving 3D heat map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-command-interface")
async def ai_command_interface():
    """Serve the AI command interface"""
    try:
        ai_interface_path = Path("ai-command-interface.html")
        if ai_interface_path.exists():
            return FileResponse(ai_interface_path)
        else:
            raise HTTPException(status_code=404, detail="AI command interface not found")
    except Exception as e:
        logger.error(f"Error serving AI command interface: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/advanced-military-map")
async def advanced_military_map():
    """Serve the tactical operations map"""
    try:
        tactical_map_path = Path("tactical-operations-map.html")
        if tactical_map_path.exists():
            return FileResponse(tactical_map_path)
        else:
            # Fallback to advanced map
            advanced_map_path = Path("advanced-military-map.html")
            if advanced_map_path.exists():
                return FileResponse(advanced_map_path)
            else:
                raise HTTPException(status_code=404, detail="Tactical map not found")
    except Exception as e:
        logger.error(f"Error serving tactical map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/working-military-map")
async def working_military_map():
    """Serve the working military map interface"""
    try:
        working_map_path = Path("working-military-map.html")
        if working_map_path.exists():
            return FileResponse(working_map_path)
        else:
            raise HTTPException(status_code=404, detail="Working military map not found")
    except Exception as e:
        logger.error(f"Error serving working military map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/real-military-map")
async def real_military_map():
    """Serve the real military map interface"""
    try:
        real_map_path = Path("real-military-map.html")
        if real_map_path.exists():
            return FileResponse(real_map_path)
        else:
            raise HTTPException(status_code=404, detail="Real military map not found")
    except Exception as e:
        logger.error(f"Error serving real military map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@app.post("/api/military-ai")
async def military_ai_command(request: dict):
    """Advanced military AI command interface with model selection"""
    try:
        command = request.get("command", "")
        ai_model = request.get("ai_model", "openai")
        location = request.get("location", "Unknown AOR")
        
        if not command:
            return {"error": "No command provided"}
        
        # Initialize response
        response = {
            "ai_model": ai_model,
            "command": command,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
        
        if ai_model == "openai":
            # OpenAI Tactical Analysis
            try:
                import requests
                import json
                
                openai_api_key = os.getenv('OPENAI_API_KEY')
                if openai_api_key:
                    tactical_prompt = f"""
                    You are a military tactical AI assistant providing strategic analysis for active operations.
                    
                    OPERATIONAL CONTEXT:
                    - Area of Responsibility: {location}
                    - Command: {command}
                    - Current Status: Active operations with heat sensor monitoring
                    
                    Provide a concise, professional military response focusing on:
                    1. Immediate tactical recommendations
                    2. Threat assessment if applicable
                    3. Asset deployment suggestions
                    4. Risk mitigation strategies
                    
                    Keep response tactical, professional, and under 200 words.
                    """
                    
                    headers = {
                        'Authorization': f'Bearer {openai_api_key}',
                        'Content-Type': 'application/json'
                    }
                    
                    payload = {
                        'model': 'gpt-4o-mini',
                        'messages': [
                            {'role': 'system', 'content': 'You are a military tactical AI providing professional battlefield analysis.'},
                            {'role': 'user', 'content': tactical_prompt}
                        ],
                        'max_tokens': 250,
                        'temperature': 0.7
                    }
                    
                    ai_response = requests.post(
                        'https://api.openai.com/v1/chat/completions',
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    if ai_response.status_code == 200:
                        ai_data = ai_response.json()
                        response["analysis"] = ai_data['choices'][0]['message']['content']
                        response["confidence"] = 0.92
                        response["system"] = "OpenAI Tactical AI GPT-4o-mini"
                    else:
                        raise Exception(f"OpenAI API error: {ai_response.status_code}")
                else:
                    raise Exception("OpenAI API key not found")
                    
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                response["analysis"] = f"""🎖️ TACTICAL AI ANALYSIS:
                
                Command: {command}
                AOR: {location}
                
                IMMEDIATE RECOMMENDATIONS:
                • Establish security perimeter around operational area
                • Deploy reconnaissance assets for threat assessment
                • Maintain communication with heat sensor network
                • Prepare contingency evacuation routes
                
                THREAT LEVEL: MODERATE
                MISSION STATUS: ACTIVE MONITORING
                
                Note: Backup tactical analysis mode active. Full AI capabilities restored shortly.
                """
                response["confidence"] = 0.75
                response["system"] = "Tactical AI (Backup Mode)"
                
        elif ai_model == "google":
            # Google AI Strategic Analysis
            try:
                import requests
                
                google_api_key = os.getenv('GOOGLE_AI_API_KEY')
                if google_api_key:
                    strategic_prompt = f"""
                    Strategic military analysis request:
                    Command: {command}
                    Location: {location}
                    
                    Provide strategic assessment covering:
                    - Long-term operational implications
                    - Intelligence considerations
                    - Strategic recommendations
                    - Diplomatic factors if relevant
                    
                    Response should be strategic, analytical, under 200 words.
                    """
                    
                    google_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={google_api_key}"
                    
                    payload = {
                        "contents": [{
                            "parts": [{
                                "text": strategic_prompt
                            }]
                        }],
                        "generationConfig": {
                            "maxOutputTokens": 250,
                            "temperature": 0.6
                        }
                    }
                    
                    google_response = requests.post(google_url, json=payload, timeout=30)
                    
                    if google_response.status_code == 200:
                        google_data = google_response.json()
                        if "candidates" in google_data:
                            response["analysis"] = google_data["candidates"][0]["content"]["parts"][0]["text"]
                            response["confidence"] = 0.89
                            response["system"] = "Google AI Strategic Intelligence"
                        else:
                            raise Exception("No response from Google AI")
                    else:
                        raise Exception(f"Google AI API error: {google_response.status_code}")
                        
                else:
                    raise Exception("Google AI API key not configured")
                    
            except Exception as e:
                response["analysis"] = f"🧠 STRATEGIC AI: Analyzing command '{command}' within broader operational context. Strategic assessment indicates need for comprehensive intelligence gathering and diplomatic coordination. Long-term success probability high with proper resource allocation."
                response["confidence"] = 0.78
                response["system"] = "Strategic AI (Backup Mode)"
                
        elif ai_model == "dual":
            # Dual AI Analysis
            response["analysis"] = f"⚡ DUAL AI ANALYSIS INITIATED for command: '{command}'\n\n🤖 TACTICAL: Immediate operational assessment shows need for enhanced security protocols and rapid response capabilities.\n\n🧠 STRATEGIC: Long-term analysis indicates successful mission outcome probability of 87% with current asset configuration."
            response["confidence"] = 0.94
            response["system"] = "Dual AI Command System"
            
        # Add tactical metadata
        response["tactical_metadata"] = {
            "priority_level": "HIGH" if any(word in command.lower() for word in ["threat", "enemy", "urgent", "immediate"]) else "MEDIUM",
            "response_time": "IMMEDIATE",
            "classification": "OPERATIONAL",
            "next_action": "AWAIT COMMANDER GUIDANCE"
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Military AI command error: {e}")
        return {
            "error": f"Military AI system error: {str(e)}",
            "backup_response": "🤖 Military AI systems experiencing temporary difficulty. Falling back to standard operating procedures.",
            "timestamp": datetime.now().isoformat()
        }

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