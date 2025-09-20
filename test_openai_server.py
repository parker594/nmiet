import requests
import json
import os

# Test the new OpenAI-only server
def test_openai_server():
    print("🧪 Testing OpenAI-Only Military AI Server...")
    
    # Test basic status
    try:
        response = requests.get("http://localhost:8002/api/military-status")
        if response.status_code == 200:
            print("✅ Server Status API working")
            data = response.json()
            print(f"   OpenAI Status: {data['ai_systems']['openai']['status']}")
        else:
            print(f"❌ Status API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Status test failed: {e}")
    
    # Test OpenAI integration
    try:
        payload = {
            "command": "Test tactical analysis",
            "location": "Pune Command Center",
            "ai_model": "openai"
        }
        
        response = requests.post(
            "http://localhost:8002/api/military-ai",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ OpenAI Military AI Response:")
            print(f"   Status: {data.get('status', 'N/A')}")
            print(f"   System: {data.get('system', 'N/A')}")
            if 'analysis' in data:
                print(f"   Analysis: {data['analysis'][:100]}...")
            else:
                print("   No analysis received")
        else:
            print(f"❌ OpenAI test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ OpenAI integration test failed: {e}")

if __name__ == "__main__":
    test_openai_server()