"""
Simple Integration Server for Military AI Simulation Demo
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Military AI Simulation", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
frontend_dir = Path(__file__).parent / "frontend"
if frontend_dir.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

# Mock AI systems
class MockNavigation:
    def get_decision(self):
        return {
            "action": "SOUTHEAST",
            "confidence": 0.85,
            "reasoning": "Optimal path with minimal threat exposure",
            "threat_level": "LOW",
            "timestamp": datetime.now().isoformat()
        }

class MockThreatDetection:
    def scan(self):
        return {
            "threats_detected": 0,
            "confidence": 0.95,
            "status": "clear",
            "scan_time": datetime.now().isoformat()
        }

class MockSwarmCoordinator:
    def get_status(self):
        return {
            "active_agents": 3,
            "missions": 1,
            "coordination_status": "optimal",
            "last_update": datetime.now().isoformat()
        }

# Initialize mock systems
nav_system = MockNavigation()
threat_system = MockThreatDetection()
swarm_system = MockSwarmCoordinator()

# WebSocket connections
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info("Client connected to WebSocket")
    
    try:
        while True:
            # Send real-time updates
            update = {
                "type": "system_update",
                "timestamp": datetime.now().isoformat(),
                "navigation": nav_system.get_decision(),
                "threats": threat_system.scan(),
                "swarm": swarm_system.get_status()
            }
            await websocket.send_text(json.dumps(update))
            await asyncio.sleep(2)  # Update every 2 seconds
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)
        logger.info("Client disconnected")

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Military AI Simulation</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #1a1a1a; color: #00ff00; }
            .container { max-width: 1200px; margin: 0 auto; }
            .system-status { background: #2a2a2a; padding: 20px; margin: 10px 0; border-radius: 5px; }
            .status-title { color: #ffff00; font-size: 20px; margin-bottom: 10px; }
            .metric { margin: 5px 0; }
            .btn { background: #004400; color: #00ff00; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #006600; }
            #log { background: #000; color: #00ff00; padding: 10px; height: 200px; overflow-y: scroll; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚁 MILITARY AI SIMULATION COMMAND CENTER 🚁</h1>
            
            <div class="system-status">
                <div class="status-title">🎯 Navigation System</div>
                <div id="nav-status">Initializing...</div>
            </div>
            
            <div class="system-status">
                <div class="status-title">🔍 Threat Detection</div>
                <div id="threat-status">Initializing...</div>
            </div>
            
            <div class="system-status">
                <div class="status-title">🤖 Swarm Coordination</div>
                <div id="swarm-status">Initializing...</div>
            </div>
            
            <div class="system-status">
                <button class="btn" onclick="testAI()">🧠 Test AI Systems</button>
                <button class="btn" onclick="startMission()">🚀 Start Mission</button>
                <button class="btn" onclick="emergencyStop()">🛑 Emergency Stop</button>
            </div>
            
            <div class="system-status">
                <div class="status-title">📊 System Log</div>
                <div id="log"></div>
            </div>
        </div>
        
        <script>
            let ws = null;
            
            function connectWebSocket() {
                ws = new WebSocket('ws://localhost:8000/ws');
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    updateStatus(data);
                };
                
                ws.onclose = function() {
                    log('WebSocket connection closed. Reconnecting...');
                    setTimeout(connectWebSocket, 3000);
                };
                
                ws.onerror = function(error) {
                    log('WebSocket error: ' + error);
                };
            }
            
            function updateStatus(data) {
                if (data.navigation) {
                    document.getElementById('nav-status').innerHTML = 
                        `Action: ${data.navigation.action}<br>
                         Confidence: ${(data.navigation.confidence * 100).toFixed(1)}%<br>
                         Threat Level: ${data.navigation.threat_level}`;
                }
                
                if (data.threats) {
                    document.getElementById('threat-status').innerHTML = 
                        `Threats: ${data.threats.threats_detected}<br>
                         Status: ${data.threats.status}<br>
                         Confidence: ${(data.threats.confidence * 100).toFixed(1)}%`;
                }
                
                if (data.swarm) {
                    document.getElementById('swarm-status').innerHTML = 
                        `Active Agents: ${data.swarm.active_agents}<br>
                         Missions: ${data.swarm.missions}<br>
                         Status: ${data.swarm.coordination_status}`;
                }
            }
            
            function log(message) {
                const logDiv = document.getElementById('log');
                const timestamp = new Date().toLocaleTimeString();
                logDiv.innerHTML += `[${timestamp}] ${message}<br>`;
                logDiv.scrollTop = logDiv.scrollHeight;
            }
            
            function testAI() {
                log('🧠 Running AI system diagnostics...');
                fetch('/api/test-ai').then(r => r.json()).then(data => {
                    log('✅ AI systems operational');
                });
            }
            
            function startMission() {
                log('🚀 Mission commenced - Operation Thunder');
                log('📡 All systems green, commencing autonomous operations');
            }
            
            function emergencyStop() {
                log('🛑 EMERGENCY STOP ACTIVATED');
                log('⚠️ All autonomous operations halted');
            }
            
            // Initialize
            connectWebSocket();
            log('🖥️ Military AI Simulation System Online');
            log('🔗 Connecting to command and control...');
        </script>
    </body>
    </html>
    """)

@app.get("/api/status")
async def get_status():
    return {
        "status": "operational",
        "systems": {
            "navigation": "online",
            "threat_detection": "online", 
            "swarm_coordination": "online"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/test-ai")
async def test_ai():
    return {
        "navigation": nav_system.get_decision(),
        "threats": threat_system.scan(),
        "swarm": swarm_system.get_status()
    }

@app.post("/api/mission/start")
async def start_mission():
    logger.info("Mission started")
    return {"status": "mission_started", "mission_id": "OP_THUNDER_001"}

@app.post("/api/emergency-stop")
async def emergency_stop():
    logger.info("Emergency stop activated")
    return {"status": "emergency_stop_activated"}

if __name__ == "__main__":
    logger.info("🚁 Starting Military AI Simulation Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")