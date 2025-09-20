"""
Main Integration Server for Military AI Simulation - OpenAI Only Version
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
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Military AI Simulation API - OpenAI Edition",
    description="Advanced tactical simulation with OpenAI-powered analysis",
    version="2.0.0"
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

# Mock data for demonstration - Pune military coordinates
heat_signatures = [
    {
        "id": "HS-001",
        "position": {"lat": 18.5204, "lng": 73.8567},
        "temperature": 89.2,
        "status": "Normal",
        "type": "Perimeter",
        "last_updated": "2024-12-19T10:30:00Z",
        "critical": False
    },
    {
        "id": "HS-002",
        "position": {"lat": 18.5304, "lng": 73.8667},
        "temperature": 94.7,
        "status": "Elevated",
        "type": "Forward Base",
        "last_updated": "2024-12-19T10:31:00Z",
        "critical": False
    },
    {
        "id": "HS-003",
        "position": {"lat": 18.5354, "lng": 73.8717},
        "temperature": 101.1,
        "status": "Critical",
        "type": "Red Zone",
        "last_updated": "2024-12-19T10:32:00Z",
        "critical": True
    },
    {
        "id": "HS-004",
        "position": {"lat": 18.5104, "lng": 73.8467},
        "temperature": 78.3,
        "status": "Normal",
        "type": "Supply Route",
        "last_updated": "2024-12-19T10:33:00Z",
        "critical": False
    },
    {
        "id": "HS-005",
        "position": {"lat": 18.5554, "lng": 73.8917},
        "temperature": 96.8,
        "status": "Critical",
        "type": "Investigation Zone",
        "last_updated": "2024-12-19T10:34:00Z",
        "critical": True
    },
    {
        "id": "HS-006",
        "position": {"lat": 18.5454, "lng": 73.8817},
        "temperature": 83.5,
        "status": "Normal",
        "type": "Checkpoint",
        "last_updated": "2024-12-19T10:35:00Z",
        "critical": False
    }
]

# Military bases and facilities in Pune area
military_assets = [
    {
        "id": "BASE-ALPHA",
        "name": "Alpha Base",
        "position": {"lat": 18.5204, "lng": 73.8567},
        "type": "Forward Operating Base",
        "personnel": 150,
        "status": "Operational",
        "equipment": ["Armored Vehicles", "Communication Array", "Medical Station"]
    },
    {
        "id": "AIRBASE-PUNE",
        "name": "Pune Airbase",
        "position": {"lat": 18.5821, "lng": 73.9197},
        "type": "Air Force Installation",
        "personnel": 300,
        "status": "Operational",
        "equipment": ["Aircraft", "Radar Systems", "Fuel Depot"]
    },
    {
        "id": "OUTPOST-BRAVO",
        "name": "Bravo Outpost",
        "position": {"lat": 18.5104, "lng": 73.8467},
        "type": "Observation Post",
        "personnel": 25,
        "status": "Active",
        "equipment": ["Surveillance Equipment", "Communications", "Defensive Weapons"]
    },
    {
        "id": "SUPPORT-CHARLIE",
        "name": "Charlie Support",
        "position": {"lat": 18.5654, "lng": 73.9017},
        "type": "Supply Depot",
        "personnel": 75,
        "status": "Operational",
        "equipment": ["Supply Storage", "Transport Vehicles", "Maintenance Facility"]
    }
]

@app.get("/")
async def home():
    """Serve the main military homepage"""
    try:
        homepage_path = Path("military-homepage.html")
        if homepage_path.exists():
            return FileResponse(homepage_path)
        else:
            # Return basic HTML if file not found
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head><title>Military AI Command Center</title></head>
            <body style="background: #001122; color: #00ff00; font-family: monospace; padding: 50px;">
                <h1>🎖️ MILITARY AI COMMAND CENTER</h1>
                <h2>🤖 OpenAI Tactical Analysis System</h2>
                <p>System Status: <span style="color: #00ff00;">OPERATIONAL</span></p>
                <ul>
                    <li><a href="/conversational-ai" style="color: #00aaff;">💬 Conversational AI Interface</a></li>
                    <li><a href="/ai-command" style="color: #00aaff;">🧠 AI Command Interface</a></li>
                    <li><a href="/tactical-map" style="color: #00aaff;">🗺️ Tactical Operations Map</a></li>
                    <li><a href="/3d-heat-map" style="color: #00aaff;">📊 3D Heat Visualization</a></li>
                    <li><a href="/api/military-status" style="color: #00aaff;">📡 System Status API</a></li>
                </ul>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving homepage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversational-ai")
async def conversational_ai():
    """Serve the conversational AI interface"""
    try:
        # Use absolute path to ensure file is found
        interface_path = Path(__file__).parent / "final-military-ai-interface.html"
        logger.info(f"Looking for interface file at: {interface_path}")
        logger.info(f"File exists: {interface_path.exists()}")
        
        if interface_path.exists():
            return FileResponse(interface_path)
        else:
            # Fallback conversational interface
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head><title>Conversational Military AI</title></head>
            <body style="background: #000; color: #00ff00; font-family: monospace; padding: 20px;">
                <h1>💬 CONVERSATIONAL MILITARY AI</h1>
                <h2>Natural Language Understanding System</h2>
                <p>Status: <span style="color: #00ff00;">OPERATIONAL</span></p>
                <div style="margin: 20px 0;">
                    <h3>Talk to me naturally - I understand context!</h3>
                    <p>You can ask me anything - no specific commands needed.</p>
                    <input type="text" id="message" placeholder="What's on your mind today?" 
                           style="width: 70%; padding: 10px; background: #001122; color: #00ff00; border: 1px solid #00ff00;">
                    <button onclick="sendMessage()" style="padding: 10px; background: #00aa00; color: white; border: none;">
                        Send
                    </button>
                </div>
                <div id="conversation" style="background: #001122; padding: 20px; margin: 20px 0; max-height: 400px; overflow-y: auto;"></div>
                <script>
                    async function sendMessage() {
                        const message = document.getElementById('message').value;
                        if (!message) return;
                        
                        const conversation = document.getElementById('conversation');
                        conversation.innerHTML += '<div style="color: #00aaff;">You: ' + message + '</div>';
                        
                        try {
                            const response = await fetch('/api/openai-chat', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({message: message})
                            });
                            const data = await response.json();
                            conversation.innerHTML += '<div style="color: #00ff00;">AI: ' + data.response + '</div>';
                        } catch (error) {
                            conversation.innerHTML += '<div style="color: #ff0000;">Error: ' + error.message + '</div>';
                        }
                        
                        document.getElementById('message').value = '';
                        conversation.scrollTop = conversation.scrollHeight;
                    }
                    
                    document.getElementById('message').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') sendMessage();
                    });
                </script>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving conversational AI interface: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-command")
async def ai_command():
    """Serve the OpenAI-only command interface"""
    try:
        ai_interface_path = Path("openai-only-interface.html")
        if ai_interface_path.exists():
            return FileResponse(ai_interface_path)
        else:
            # Fallback AI interface
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head><title>AI Command Interface</title></head>
            <body style="background: #000; color: #00ff00; font-family: monospace; padding: 20px;">
                <h1>🤖 AI COMMAND INTERFACE</h1>
                <h2>OpenAI GPT-4o-mini Tactical System</h2>
                <p>Status: <span style="color: #00ff00;">OPERATIONAL</span></p>
                <div style="margin: 20px 0;">
                    <input type="text" id="command" placeholder="Enter tactical command..." 
                           style="width: 70%; padding: 10px; background: #001122; color: #00ff00; border: 1px solid #00ff00;">
                    <button onclick="sendCommand()" style="padding: 10px; background: #00aa00; color: white; border: none;">
                        Send Command
                    </button>
                </div>
                <div id="response" style="background: #001122; padding: 15px; margin: 20px 0; border: 1px solid #00ff00; min-height: 200px;"></div>
                <script>
                    async function sendCommand() {
                        const command = document.getElementById('command').value;
                        if (!command) return;
                        
                        const response = await fetch('/api/military-ai', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({command: command, ai_model: 'openai'})
                        });
                        
                        const data = await response.json();
                        document.getElementById('response').innerHTML = 
                            '<strong>AI Analysis:</strong><br>' + (data.analysis || 'No response');
                        document.getElementById('command').value = '';
                    }
                </script>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving AI command interface: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tactical-map")
async def tactical_map():
    """Serve the tactical operations map"""
    try:
        tactical_map_path = Path("tactical-operations-map.html")
        if tactical_map_path.exists():
            return FileResponse(tactical_map_path)
        else:
            raise HTTPException(status_code=404, detail="Tactical map not found")
    except Exception as e:
        logger.error(f"Error serving tactical map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/api/military-status")
async def military_status():
    """Get current military system status"""
    try:
        openai_key = os.getenv('OPENAI_API_KEY')
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_status": "OPERATIONAL",
            "ai_systems": {
                "openai": {
                    "status": "READY" if openai_key else "NOT_CONFIGURED",
                    "model": "GPT-4o-mini",
                    "capabilities": ["Tactical Analysis", "Strategic Planning", "Threat Assessment"]
                }
            },
            "heat_sensors": {
                "total": len(heat_signatures),
                "active": len([h for h in heat_signatures if h["status"] != "Offline"]),
                "critical": len([h for h in heat_signatures if h["critical"]])
            },
            "military_assets": {
                "total_bases": len(military_assets),
                "operational": len([a for a in military_assets if a["status"] == "Operational"]),
                "total_personnel": sum(a["personnel"] for a in military_assets)
            },
            "operational_area": "Pune Military Command Zone",
            "security_level": "ALPHA",
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/heat-signatures")
async def get_heat_signatures():
    """Get all heat signature data"""
    try:
        return {
            "signatures": heat_signatures,
            "summary": {
                "total": len(heat_signatures),
                "critical": len([h for h in heat_signatures if h["critical"]]),
                "average_temp": sum(h["temperature"] for h in heat_signatures) / len(heat_signatures),
                "max_temp": max(h["temperature"] for h in heat_signatures),
                "min_temp": min(h["temperature"] for h in heat_signatures)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting heat signatures: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/military-assets")
async def get_military_assets():
    """Get all military asset data"""
    try:
        return {
            "assets": military_assets,
            "summary": {
                "total_bases": len(military_assets),
                "total_personnel": sum(a["personnel"] for a in military_assets),
                "operational_status": {
                    "operational": len([a for a in military_assets if a["status"] == "Operational"]),
                    "active": len([a for a in military_assets if a["status"] == "Active"]),
                    "total": len(military_assets)
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting military assets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class MilitaryAIRequest:
    def __init__(self, command: str, location: str = "Unknown", ai_model: str = "openai"):
        self.command = command
        self.location = location
        self.ai_model = ai_model

@app.post("/api/military-ai")
async def military_ai_analysis(request: dict):
    """Enhanced AI-powered military tactical analysis - OpenAI Only"""
    try:
        command = request.get("command", "")
        location = request.get("location", "Pune Military Command Center")
        ai_model = request.get("ai_model", "openai").lower()

        if not command:
            raise HTTPException(status_code=400, detail="Command is required")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Initialize response
        response = {
            "timestamp": timestamp,
            "command": command,
            "location": location,
            "ai_model": ai_model,
            "analysis": "",
            "system": "OpenAI Military Intelligence",
            "threat_level": "MODERATE",
            "recommendations": []
        }

        # Only OpenAI is supported now
        if ai_model == "openai":
            # OpenAI Tactical Analysis
            logger.info(f"Processing OpenAI request: {command}")
            try:
                openai_api_key = os.getenv('OPENAI_API_KEY')
                if openai_api_key:
                    # Natural conversation with military focus
                    military_prompt = f"""You are an intelligent military AI assistant at the Pune Military Command Center. 

PERSONALITY:
- Conversational and natural, but professional
- Understand context and respond appropriately to any question
- When topics go off-military, gently relate back to military/tactical matters
- Remember conversation context and build on it
- Knowledgeable about military operations and procedures

CURRENT MILITARY CONTEXT:
- Base: Pune Military Command Center
- Location: {location}
- Coordinates: 18.5204°N, 73.8567°E
- Operations: Heat monitoring, Perimeter security, Intelligence gathering
- Status: Operational readiness level ALPHA
- Assets: 4 military bases, 6 heat sensors, 550+ personnel

CURRENT SITUATION:
- Heat Sensor HS-003: 101.1°F (Critical) - Red Zone
- Heat Sensor HS-005: 96.8°F (Critical) - Investigation Zone
- Other sensors: Normal operational ranges
- All military assets: Fully operational

USER MESSAGE: "{command}"

RESPONSE GUIDELINES:
1. Respond naturally to whatever the user is saying
2. If it's off-topic, acknowledge it but relate it back to military context when appropriate
3. Be conversational - ask follow-up questions, show interest
4. Use military knowledge when relevant but don't force it
5. Keep responses helpful and engaging
6. Remember this is part of an ongoing conversation

Respond naturally and intelligently to the user's message."""

                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are an intelligent military AI assistant. Respond naturally and conversationally while maintaining military professionalism. Understand context and provide helpful, engaging responses."
                            },
                            {
                                "role": "user",
                                "content": military_prompt
                            }
                        ],
                        "max_tokens": 600,
                        "temperature": 0.8
                    }

                    headers = {
                        "Authorization": f"Bearer {openai_api_key}",
                        "Content-Type": "application/json"
                    }

                    openai_response = requests.post(
                        "https://api.openai.com/v1/chat/completions",
                        json=payload,
                        headers=headers,
                        timeout=30
                    )

                    if openai_response.status_code == 200:
                        openai_data = openai_response.json()
                        if "choices" in openai_data and len(openai_data["choices"]) > 0:
                            response["analysis"] = openai_data["choices"][0]["message"]["content"]
                            response["model"] = "GPT-4o-mini"
                            response["system"] = "OpenAI Military Intelligence"
                            response["status"] = "SUCCESS"
                        else:
                            raise Exception("No response from OpenAI")
                    else:
                        logger.error(f"OpenAI API error: {openai_response.status_code} - {openai_response.text}")
                        raise Exception(f"OpenAI API error: {openai_response.status_code}")
                        
                else:
                    raise Exception("OpenAI API key not configured")

            except Exception as e:
                logger.error(f"OpenAI request failed: {e}")
                # Provide intelligent fallback response
                response["analysis"] = generate_tactical_fallback(command, location)
                response["system"] = "Backup Military Intelligence"
                response["status"] = "FALLBACK"

        else:
            # Only OpenAI is supported
            response["analysis"] = f"⚠️ Only OpenAI tactical analysis is available. Google AI has been decommissioned due to quota limitations.\n\nPlease use ai_model='openai' for tactical analysis."
            response["system"] = "System Notice"
            response["status"] = "ERROR"

        return response

    except Exception as e:
        logger.error(f"Military AI analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_tactical_fallback(command: str, location: str) -> str:
    """Generate intelligent tactical fallback response"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    cmd = command.lower()
    
    base_response = f"""🎖️ TACTICAL ANALYSIS REPORT [{timestamp}]
📍 LOCATION: {location}
🎯 COMMAND: {command}

OPERATIONAL STATUS:
✅ Military Command Systems: OPERATIONAL
✅ Heat Sensor Network: 6 sensors active
⚠️ Critical Readings: 2 sensors requiring attention
✅ Communication Systems: FULLY FUNCTIONAL

"""
    
    if any(word in cmd for word in ['threat', 'assess', 'analysis', 'situation']):
        return base_response + """THREAT ASSESSMENT:
• Current Threat Level: MODERATE to HIGH
• Active Monitoring: Heat signatures in Red Zone (101.1°F)
• Investigation Required: Zone HS-005 (96.8°F)
• Personnel Status: All 550+ personnel accounted for

IMMEDIATE RECOMMENDATIONS:
1. Maintain elevated security posture
2. Continue monitoring critical heat sensors
3. Deploy investigation team to high-temp zones
4. Establish communication with forward positions

TACTICAL PRIORITY: Monitor and investigate thermal anomalies"""
    
    elif any(word in cmd for word in ['deploy', 'position', 'tactical', 'strategy']):
        return base_response + """DEPLOYMENT STRATEGY:
• Primary Force: Alpha Base (150 personnel) - Forward positions
• Air Support: Pune Airbase (300 personnel) - Ready status
• Reconnaissance: Bravo Outpost (25 personnel) - Active patrol
• Logistics: Charlie Support (75 personnel) - Supply secured

TACTICAL POSITIONING:
• Heat Sensor Coverage: Complete operational area
• Communication Network: Redundant systems active
• Evacuation Routes: Multiple pathways secured
• Emergency Response: All teams on standby

DEPLOYMENT STATUS: Ready for immediate action"""
    
    elif any(word in cmd for word in ['heat', 'sensor', 'temperature', 'thermal']):
        return base_response + """HEAT SENSOR ANALYSIS:
• HS-001: 89.2°F - NORMAL (Perimeter secure)
• HS-002: 94.7°F - ELEVATED (Monitor closely)
• HS-003: 101.1°F - CRITICAL (Immediate investigation)
• HS-004: 78.3°F - NORMAL (Supply route clear)
• HS-005: 96.8°F - CRITICAL (Deploy investigation team)
• HS-006: 83.5°F - NORMAL (Checkpoint operational)

THERMAL ANALYSIS:
• Average Temperature: 90.3°F
• Critical Zones: 2 locations requiring attention
• Trend Analysis: Elevated readings in sectors 3 & 5

PRIORITY ACTION: Investigate critical temperature zones"""
    
    else:
        return base_response + """GENERAL MILITARY STATUS:
• All systems operational and mission-ready
• Personnel: 550+ military assets deployed
• Equipment: Full combat readiness maintained
• Intelligence: Continuous monitoring active

CURRENT OPERATIONS:
• Perimeter security: ACTIVE
• Heat monitoring: CONTINUOUS
• Communication: SECURE CHANNELS
• Logistics: SUPPLY LINES OPEN

READY FOR: Additional tactical guidance and mission execution

Awaiting further orders from command authority."""

if __name__ == "__main__":
    logger.info("🎖️ Starting Military AI Simulation Server - OpenAI Edition")
    uvicorn.run(app, host="0.0.0.0", port=8002)