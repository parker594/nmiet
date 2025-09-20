#!/usr/bin/env python3
"""
Test AI APIs directly to diagnose issues
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test OpenAI API directly"""
    print("🤖 Testing OpenAI API...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-4o-mini',
            'messages': [
                {'role': 'system', 'content': 'You are a military tactical AI.'},
                {'role': 'user', 'content': 'Provide a brief tactical assessment of a secure perimeter.'}
            ],
            'max_tokens': 100,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            analysis = data['choices'][0]['message']['content']
            print("✅ OpenAI API working!")
            print(f"Response: {analysis[:100]}...")
            return True
        else:
            print(f"❌ OpenAI API failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

def test_google_ai_api():
    """Test Google AI API directly"""
    print("\n🧠 Testing Google AI API...")
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print("❌ Google AI API key not found")
        return False
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Provide a brief strategic military assessment in 50 words."
                }]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                analysis = data['candidates'][0]['content']['parts'][0]['text']
                print("✅ Google AI API working!")
                print(f"Response: {analysis[:100]}...")
                return True
            else:
                print("❌ No response from Google AI")
                return False
        else:
            print(f"❌ Google AI API failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Google AI API error: {e}")
        return False

def test_local_server():
    """Test the local tactical server"""
    print("\n🖥️ Testing local tactical server...")
    
    try:
        # Test basic endpoint
        response = requests.get('http://localhost:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server responded with: {response.status_code}")
            return False
            
        # Test AI endpoint
        ai_payload = {
            "command": "test tactical analysis",
            "location": "Pune Command",
            "ai_model": "openai"
        }
        
        ai_response = requests.post(
            'http://localhost:8000/api/military-ai',
            json=ai_payload,
            timeout=10
        )
        
        if ai_response.status_code == 200:
            data = ai_response.json()
            print("✅ AI endpoint working!")
            print(f"Response: {json.dumps(data, indent=2)[:200]}...")
            return True
        else:
            print(f"❌ AI endpoint failed: {ai_response.status_code}")
            print(f"Error: {ai_response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Server test error: {e}")
        return False

if __name__ == "__main__":
    print("🔬 AI System Diagnostics")
    print("=" * 50)
    
    # Test APIs
    openai_ok = test_openai_api()
    google_ok = test_google_ai_api()
    server_ok = test_local_server()
    
    print("\n📊 Test Results:")
    print(f"OpenAI API: {'✅ Working' if openai_ok else '❌ Failed'}")
    print(f"Google AI API: {'✅ Working' if google_ok else '❌ Failed'}")
    print(f"Local Server: {'✅ Working' if server_ok else '❌ Failed'}")
    
    if not (openai_ok or google_ok):
        print("\n⚠️ No AI APIs are working! Check your API keys in .env file")
    elif not server_ok:
        print("\n⚠️ Server issues detected. Check the tactical_server.py")
    else:
        print("\n🎉 All systems operational!")