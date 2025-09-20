import requests
import json

# Simple test of the OpenAI API directly
def test_openai_directly():
    print("🧪 Testing OpenAI API directly...")
    
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No OpenAI API key found")
            return
            
        print(f"✅ API Key found (length: {len(api_key)})")
        
        # Test OpenAI API directly
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "Respond with 'OpenAI is working for military AI simulation'"
                }
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            message = data["choices"][0]["message"]["content"]
            print(f"✅ OpenAI Response: {message}")
        else:
            print(f"❌ OpenAI Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_openai_directly()