#!/usr/bin/env python3
"""
Test AI Endpoints - Demonstrate AI Functionality
"""

import requests
import json
import time

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

def test_ai_endpoints():
    """Test all AI-powered endpoints"""
    
    base_url = "http://localhost:8000"
    
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("🤖 MILITARY AI SIMULATION - AI DEMO")
    print("=" * 60)
    print(f"{Colors.END}")
    
    # Test 1: Tactical Analysis (AI-Powered)
    print(f"{Colors.CYAN}🧠 Testing AI Tactical Analysis{Colors.END}")
    print("-" * 40)
    
    tactical_data = {
        "situation": "Enemy convoy detected moving towards our position. 3 armored vehicles, estimated 12 personnel. Terrain: urban environment with multiple escape routes.",
        "location": "Baghdad, Iraq",
        "threat_level": "high"
    }
    
    try:
        response = requests.post(f"{base_url}/api/tactical-analysis", 
                               json=tactical_data, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"{Colors.GREEN}✅ AI Analysis Successful!{Colors.END}")
            print(f"\n{Colors.YELLOW}🎯 AI Recommendation:{Colors.END}")
            print(f"{result.get('analysis', 'No analysis available')}")
            print(f"\n{Colors.YELLOW}⚡ Threat Assessment:{Colors.END}")
            print(f"{result.get('threat_assessment', 'No assessment available')}")
            print(f"\n{Colors.YELLOW}📋 Suggested Actions:{Colors.END}")
            actions = result.get('suggested_actions', [])
            for i, action in enumerate(actions, 1):
                print(f"   {i}. {action}")
        else:
            print(f"{Colors.RED}❌ AI Analysis Failed: {response.status_code}{Colors.END}")
            print(response.text)
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing tactical analysis: {e}{Colors.END}")
    
    print("\n" + "=" * 60)
    
    # Test 2: Route Optimization (AI-Powered)
    print(f"{Colors.CYAN}🗺️ Testing AI Route Optimization{Colors.END}")
    print("-" * 40)
    
    route_data = {
        "start": "40.7128,-74.0060",  # New York
        "end": "40.7589,-73.9851",    # Times Square
        "waypoints": ["40.7505,-73.9934"],  # Central Park
        "avoid_threats": True,
        "vehicle_type": "armored"
    }
    
    try:
        response = requests.post(f"{base_url}/api/optimal-route", 
                               json=route_data, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"{Colors.GREEN}✅ AI Route Optimization Successful!{Colors.END}")
            print(f"\n{Colors.YELLOW}🛣️ Optimized Route:{Colors.END}")
            route = result.get('route', {})
            print(f"   Distance: {route.get('distance', 'Unknown')}")
            print(f"   Estimated Time: {route.get('duration', 'Unknown')}")
            print(f"   Safety Score: {route.get('safety_score', 'Unknown')}/10")
            
            print(f"\n{Colors.YELLOW}⚠️ AI Threat Assessment:{Colors.END}")
            threats = result.get('threats', [])
            if threats:
                for threat in threats:
                    print(f"   🔴 {threat}")
            else:
                print(f"   {Colors.GREEN}✅ No major threats detected on route{Colors.END}")
                
        else:
            print(f"{Colors.RED}❌ Route Optimization Failed: {response.status_code}{Colors.END}")
            print(response.text)
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing route optimization: {e}{Colors.END}")
    
    print("\n" + "=" * 60)
    
    # Test 3: Heat Signatures (Simulated AI Detection)
    print(f"{Colors.CYAN}🌡️ Testing AI Heat Signature Detection{Colors.END}")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/heat-signatures", timeout=10)
        
        if response.status_code == 200:
            signatures = response.json()
            print(f"{Colors.GREEN}✅ AI Heat Detection Active!{Colors.END}")
            print(f"\n{Colors.YELLOW}🔍 Detected Heat Signatures:{Colors.END}")
            
            for i, sig in enumerate(signatures[:5], 1):  # Show first 5
                lat = sig.get('lat', 0)
                lng = sig.get('lng', 0)
                intensity = sig.get('intensity', 0)
                print(f"   {i}. Position: ({lat:.4f}, {lng:.4f}) | Intensity: {intensity:.1f}")
                
        else:
            print(f"{Colors.RED}❌ Heat Detection Failed: {response.status_code}{Colors.END}")
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing heat detection: {e}{Colors.END}")
    
    print("\n" + "=" * 60)
    print(f"{Colors.GREEN}{Colors.BOLD}🎯 AI DEMONSTRATION COMPLETE!{Colors.END}")
    print(f"{Colors.BLUE}Visit http://localhost:8000/tactical-map to see the full AI interface{Colors.END}")
    print("=" * 60)

if __name__ == "__main__":
    test_ai_endpoints()