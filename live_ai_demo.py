#!/usr/bin/env python3
"""
Direct AI Demo - Show actual AI responses
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def demo_military_ai():
    """Demonstrate AI functionality directly"""
    
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("🤖 MILITARY AI SIMULATION - LIVE AI DEMO")
    print("=" * 60)
    print(f"{Colors.END}")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Scenario 1: Tactical Analysis
    print(f"{Colors.CYAN}🧠 AI TACTICAL ANALYSIS{Colors.END}")
    print("-" * 40)
    
    scenario = """
    MILITARY SITUATION REPORT:
    - Enemy convoy detected: 3 armored vehicles, 12 personnel
    - Location: Urban environment, Baghdad, Iraq
    - Threat level: HIGH
    - Our forces: 2 squads, defensive position
    - Terrain: Multiple escape routes available
    
    Provide tactical analysis and recommendations.
    """
    
    try:
        print(f"{Colors.YELLOW}📊 Analyzing scenario with AI...{Colors.END}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a military tactical AI assistant. Provide concise, professional tactical analysis and recommendations."},
                {"role": "user", "content": scenario}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        ai_analysis = response.choices[0].message.content
        print(f"\n{Colors.GREEN}🎯 AI TACTICAL RECOMMENDATION:{Colors.END}")
        print(f"{ai_analysis}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ AI Analysis Error: {e}{Colors.END}")
    
    print("\n" + "=" * 60)
    
    # Scenario 2: Threat Assessment
    print(f"{Colors.CYAN}⚠️ AI THREAT ASSESSMENT{Colors.END}")
    print("-" * 40)
    
    threat_scenario = """
    THREAT DETECTION REPORT:
    - Heat signatures detected: 8 human, 2 vehicle
    - Movement pattern: Coordinated advance
    - Time: 03:30 hours (night operation)
    - Weather: Clear, low visibility
    - Distance: 500 meters from base
    
    Assess threat level and recommend immediate actions.
    """
    
    try:
        print(f"{Colors.YELLOW}🔍 Processing threat data with AI...{Colors.END}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a military threat assessment AI. Analyze threats and provide immediate action recommendations."},
                {"role": "user", "content": threat_scenario}
            ],
            max_tokens=250,
            temperature=0.5
        )
        
        threat_analysis = response.choices[0].message.content
        print(f"\n{Colors.RED}🚨 AI THREAT ASSESSMENT:{Colors.END}")
        print(f"{threat_analysis}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Threat Assessment Error: {e}{Colors.END}")
    
    print("\n" + "=" * 60)
    
    # Scenario 3: Route Optimization
    print(f"{Colors.CYAN}🗺️ AI ROUTE OPTIMIZATION{Colors.END}")
    print("-" * 40)
    
    route_scenario = """
    MISSION PARAMETERS:
    - Start: Forward Operating Base Alpha
    - Destination: Extraction Point Bravo
    - Distance: 15km through hostile territory
    - Vehicle: Armored personnel carrier
    - Crew: 6 personnel
    - Known threats: Sniper positions, IED risk areas
    - Time constraint: 45 minutes maximum
    
    Optimize route for safety and speed.
    """
    
    try:
        print(f"{Colors.YELLOW}🛣️ Calculating optimal route with AI...{Colors.END}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a military route planning AI. Optimize routes for safety, speed, and mission success."},
                {"role": "user", "content": route_scenario}
            ],
            max_tokens=250,
            temperature=0.6
        )
        
        route_plan = response.choices[0].message.content
        print(f"\n{Colors.GREEN}🎯 AI ROUTE OPTIMIZATION:{Colors.END}")
        print(f"{route_plan}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Route Optimization Error: {e}{Colors.END}")
    
    print("\n" + "=" * 60)
    print(f"{Colors.GREEN}{Colors.BOLD}✅ AI DEMONSTRATION COMPLETE!{Colors.END}")
    print(f"{Colors.BLUE}Your military AI simulation is powered by:{Colors.END}")
    print(f"  🤖 OpenAI GPT-4o-mini for tactical analysis")
    print(f"  🧠 Google AI Gemini for additional intelligence")
    print(f"  🗺️ Google Maps for geospatial data")
    print(f"  🔥 Real-time heat signature detection")
    print(f"  📊 Live tactical visualization")
    print("=" * 60)

if __name__ == "__main__":
    demo_military_ai()