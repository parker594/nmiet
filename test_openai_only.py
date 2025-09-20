#!/usr/bin/env python3
"""
Simple OpenAI API test
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_simple():
    """Test OpenAI API with a simple request"""
    print("🤖 Testing OpenAI API...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found in .env file")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-4o-mini',
            'messages': [
                {'role': 'user', 'content': 'Say "AI working" if you can read this.'}
            ],
            'max_tokens': 10,
            'temperature': 0.1
        }
        
        print("📡 Sending request to OpenAI...")
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            message = data['choices'][0]['message']['content']
            print(f"✅ OpenAI Response: {message}")
            return True
        else:
            print(f"❌ OpenAI API Error: {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    test_openai_simple()