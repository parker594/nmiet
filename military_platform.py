#!/usr/bin/env python3
"""
Military AI Simulation Platform - Clean Architecture
Organized feature-based routing with proper file structure
"""

import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Military AI Simulation Platform", 
    version="2.0.0",
    description="Clean architecture with organized features"
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatMessage(BaseModel):
    message: str

# ============ MAIN ROUTES ============

@app.get("/")
async def homepage():
    """Military AI Command Center Homepage"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🎖️ Military AI Command Center</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #000 0%, #001122 50%, #000033 100%);
                color: #00ff00;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 50px;
            }
            
            .header h1 {
                font-size: 4rem;
                color: #00ff00;
                text-shadow: 0 0 30px #00ff00;
                margin-bottom: 20px;
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow {
                from { text-shadow: 0 0 20px #00ff00; }
                to { text-shadow: 0 0 40px #00ff00, 0 0 60px #00ff00; }
            }
            
            .subtitle {
                font-size: 1.5rem;
                color: #00aaff;
                margin-bottom: 10px;
            }
            
            .status {
                color: #00ff00;
                font-size: 1.2rem;
                font-weight: bold;
            }
            
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                max-width: 1200px;
                width: 100%;
            }
            
            .feature-card {
                background: rgba(0, 100, 0, 0.1);
                border: 2px solid #00ff00;
                border-radius: 15px;
                padding: 30px;
                text-align: center;
                transition: all 0.3s ease;
                cursor: pointer;
                text-decoration: none;
                color: inherit;
            }
            
            .feature-card:hover {
                background: rgba(0, 255, 0, 0.2);
                border-color: #00aaff;
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 255, 0, 0.3);
            }
            
            .feature-icon {
                font-size: 4rem;
                margin-bottom: 20px;
                display: block;
            }
            
            .feature-title {
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 15px;
                color: #00aaff;
            }
            
            .feature-description {
                font-size: 1rem;
                line-height: 1.6;
                color: #cccccc;
            }
            
            .footer {
                margin-top: 50px;
                text-align: center;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎖️ MILITARY AI COMMAND CENTER</h1>
            <div class="subtitle">Advanced Tactical Intelligence Platform</div>
            <div class="status">🟢 ALL SYSTEMS OPERATIONAL</div>
        </div>
        
        <div class="features-grid">
            <a href="/ai-chat" class="feature-card">
                <span class="feature-icon">🤖</span>
                <div class="feature-title">AI Chat Assistant</div>
                <div class="feature-description">
                    Natural language conversation with military AI. 
                    Get intelligence analysis, tactical advice, and strategic insights.
                </div>
            </a>
            
            <a href="/tactical-map" class="feature-card">
                <span class="feature-icon">🗺️</span>
                <div class="feature-title">Tactical Operations Map</div>
                <div class="feature-description">
                    Interactive battlefield visualization with real-time unit tracking,
                    mission planning, and strategic positioning.
                </div>
            </a>
            
            <a href="/heat-visualization" class="feature-card">
                <span class="feature-icon">📊</span>
                <div class="feature-title">3D Heat Visualization</div>
                <div class="feature-description">
                    Advanced 3D thermal analysis for threat detection,
                    environmental monitoring, and tactical advantage.
                </div>
            </a>
            
            <a href="/command-center" class="feature-card">
                <span class="feature-icon">⚡</span>
                <div class="feature-title">Command Center</div>
                <div class="feature-description">
                    Central command interface for mission control,
                    communication systems, and operational oversight.
                </div>
            </a>
        </div>
        
        <div class="footer">
            <p>🔒 Secure Military-Grade Platform | 🤖 Powered by OpenAI GPT-4 | 🌐 Real-time Intelligence</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ============ FEATURE ROUTES ============

@app.get("/ai-chat")
async def ai_chat():
    """AI Chat Assistant Feature"""
    try:
        file_path = Path("features/ai-chat/index.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="AI Chat feature not found")
    except Exception as e:
        logger.error(f"Error serving AI Chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tactical-map")
async def tactical_map():
    """Tactical Operations Map Feature"""
    try:
        file_path = Path("features/tactical-map/index.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="Tactical Map feature not found")
    except Exception as e:
        logger.error(f"Error serving Tactical Map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/heat-visualization")
async def heat_visualization():
    """3D Heat Visualization Feature"""
    try:
        file_path = Path("features/heat-visualization/index.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="Heat Visualization feature not found")
    except Exception as e:
        logger.error(f"Error serving Heat Visualization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/command-center")
async def command_center():
    """Command Center Feature"""
    # For now, redirect to the best command interface we have
    try:
        file_path = Path("openai-only-interface.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            return HTMLResponse(content="""
            <!DOCTYPE html>
            <html>
            <head><title>Command Center - Coming Soon</title></head>
            <body style="background: #000; color: #00ff00; font-family: monospace; padding: 50px; text-align: center;">
                <h1>🏗️ Command Center Under Development</h1>
                <p>This feature is being built. Please use other available features.</p>
                <a href="/" style="color: #00aaff;">← Back to Homepage</a>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving Command Center: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============ LEGACY REDIRECT ROUTES ============

@app.get("/military-homepage.html")
async def legacy_homepage_redirect():
    """Redirect old homepage requests to new root"""
    return HTMLResponse(content="""
    <script>window.location.href = '/';</script>
    <p>Redirecting to homepage...</p>
    """)

@app.get("/tactical-operations-map.html")
async def legacy_tactical_map_redirect():
    """Redirect old tactical map requests to new route"""
    return HTMLResponse(content="""
    <script>window.location.href = '/tactical-map';</script>
    <p>Redirecting to tactical map...</p>
    """)

@app.get("/3d-heat-map.html")
async def legacy_heat_map_redirect():
    """Redirect old heat map requests to new route"""
    return HTMLResponse(content="""
    <script>window.location.href = '/heat-visualization';</script>
    <p>Redirecting to heat visualization...</p>
    """)

# ============ API ENDPOINTS ============

@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    """AI Chat API - Clean endpoint for conversational AI"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a military AI assistant with deep expertise in:
                    - Tactical operations and strategic planning
                    - Intelligence analysis and threat assessment  
                    - Military technology and equipment
                    - Battlefield communications and logistics
                    - Security protocols and operational procedures
                    
                    Respond naturally and conversationally while maintaining your military focus. 
                    You can discuss any topic but always provide military perspective when relevant.
                    Be helpful, precise, and professional."""
                },
                {"role": "user", "content": message.message}
            ],
            max_tokens=600,
            temperature=0.7
        )
        
        return {"response": response.choices[0].message.content}
        
    except Exception as e:
        logger.error(f"AI Chat API error: {e}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

@app.get("/api/status")
async def system_status():
    """System status endpoint"""
    return {
        "status": "operational",
        "features": {
            "ai_chat": "active",
            "tactical_map": "active", 
            "heat_visualization": "active",
            "command_center": "development"
        },
        "ai_model": "gpt-4o-mini",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    logger.info("🎖️ Starting Military AI Platform - Clean Architecture")
    uvicorn.run(app, host="0.0.0.0", port=8004)