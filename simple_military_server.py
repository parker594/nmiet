#!/usr/bin/env python3
"""
Simple Military AI Server - Clean Version
Just serves HTML files and AI chat without complications
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

app = FastAPI(title="Military AI Simulation", version="1.0.0")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatMessage(BaseModel):
    message: str

@app.get("/")
async def home():
    """Simple homepage with links to all features"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎖️ Military AI Command Center</title>
        <style>
            body { 
                background: #001122; 
                color: #00ff00; 
                font-family: monospace; 
                padding: 50px; 
                text-align: center;
            }
            h1 { 
                font-size: 3rem; 
                color: #00ff00; 
                text-shadow: 0 0 20px #00ff00; 
                margin-bottom: 30px;
            }
            .menu { 
                list-style: none; 
                padding: 0;
                margin: 30px 0;
            }
            .menu li { 
                margin: 15px 0; 
            }
            .menu a { 
                color: #00aaff; 
                text-decoration: none; 
                font-size: 1.2rem;
                padding: 10px 20px;
                border: 1px solid #00aaff;
                border-radius: 5px;
                display: inline-block;
                transition: all 0.3s;
            }
            .menu a:hover { 
                background: #00aaff; 
                color: #000; 
            }
        </style>
    </head>
    <body>
        <h1>🎖️ MILITARY AI COMMAND CENTER</h1>
        <h2>🤖 All Systems Operational</h2>
        
        <ul class="menu">
            <li><a href="/conversational-ai">💬 Conversational AI Chat</a></li>
            <li><a href="/tactical-map">🗺️ Tactical Operations Map</a></li>
            <li><a href="/3d-heat-map">📊 3D Heat Visualization</a></li>
            <li><a href="/ai-command">🧠 AI Command Interface</a></li>
        </ul>
        
        <p style="color: #00aa00; margin-top: 40px;">
            Status: <strong>OPERATIONAL</strong> | 
            AI Model: <strong>OpenAI GPT-4</strong>
        </p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/conversational-ai")
async def conversational_ai():
    """Serve the conversational AI interface"""
    try:
        file_path = Path("final-military-ai-interface.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="Conversational AI interface not found")
    except Exception as e:
        logger.error(f"Error serving conversational AI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tactical-map")
async def tactical_map():
    """Serve the tactical operations map"""
    try:
        file_path = Path("tactical-operations-map.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="Tactical map not found")
    except Exception as e:
        logger.error(f"Error serving tactical map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/3d-heat-map")
async def heat_map():
    """Serve the 3D heat map visualization"""
    try:
        file_path = Path("3d-heat-map.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="3D heat map not found")
    except Exception as e:
        logger.error(f"Error serving 3D heat map: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai-command")
async def ai_command():
    """Serve the AI command interface"""
    try:
        file_path = Path("openai-only-interface.html")
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="AI command interface not found")
    except Exception as e:
        logger.error(f"Error serving AI command interface: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/openai-chat")
async def chat_with_openai(message: ChatMessage):
    """Handle chat with OpenAI"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a military AI assistant with expertise in tactical operations, intelligence analysis, and strategic planning. Respond naturally and conversationally while maintaining your military focus. You can discuss any topic but always bring military perspective when relevant."
                },
                {"role": "user", "content": message.message}
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        return {"response": response.choices[0].message.content}
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

if __name__ == "__main__":
    logger.info("🎖️ Starting Simple Military AI Server")
    uvicorn.run(app, host="0.0.0.0", port=8003)