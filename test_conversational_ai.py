import requests
import json

def test_conversational_ai():
    """Test the conversational AI server"""
    print("🧪 Testing Conversational Military AI...")
    
    test_messages = [
        "Hello, how are you?",
        "What's the weather like today?", 
        "Tell me about our current situation",
        "I'm feeling a bit stressed about the mission",
        "Can you help me understand the heat sensor data?"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Test {i} ---")
        print(f"👤 USER: {message}")
        
        try:
            response = requests.post(
                "http://localhost:8002/api/military-ai",
                json={
                    "command": message,
                    "location": "Pune Command Center",
                    "ai_model": "openai"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('analysis', 'No response')
                print(f"🤖 AI: {ai_response[:150]}...")
                print(f"✅ Status: {response.status_code}")
            else:
                print(f"❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_conversational_ai()