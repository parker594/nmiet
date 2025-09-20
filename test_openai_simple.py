#!/usr/bin/env python3
"""
Simple OpenAI API Test with Free Models
"""

import os
import requests
import json
from dotenv import load_dotenv

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

def test_openai_free_models():
    """Test OpenAI API with different free models"""
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ OpenAI API key not found{Colors.END}")
        return False
    
    print(f"{Colors.BLUE}{Colors.BOLD}🤖 Testing OpenAI Free Models{Colors.END}")
    print("-" * 50)
    
    # Free models to test (from cheapest to most expensive)
    models = [
        ("gpt-4o-mini", "Newest free model (recommended)"),
        ("gpt-3.5-turbo", "Standard free model"),
        ("gpt-3.5-turbo-instruct", "Completion model")
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    for model, description in models:
        print(f"\n🧪 Testing {Colors.CYAN}{model}{Colors.END} - {description}")
        
        try:
            # Simple test message
            data = {
                'model': model,
                'messages': [
                    {'role': 'user', 'content': 'Say "AI test successful" if you can read this.'}
                ],
                'max_tokens': 10,
                'temperature': 0
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"   {Colors.GREEN}✅ Success: {message.strip()}{Colors.END}")
                
                # Update the .env file with the working model
                update_env_model(model)
                return True
                
            elif response.status_code == 429:
                print(f"   {Colors.YELLOW}⚠️ Rate limited - try again in a few minutes{Colors.END}")
                
            elif response.status_code == 401:
                print(f"   {Colors.RED}❌ Invalid API key{Colors.END}")
                
            elif response.status_code == 404:
                print(f"   {Colors.YELLOW}⚠️ Model not available{Colors.END}")
                
            else:
                print(f"   {Colors.RED}❌ HTTP {response.status_code}: {response.text[:100]}{Colors.END}")
                
        except Exception as e:
            print(f"   {Colors.RED}❌ Error: {str(e)}{Colors.END}")
    
    return False

def update_env_model(model):
    """Update the .env file with the working model"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace the model line
        import re
        content = re.sub(r'OPENAI_MODEL=.*', f'OPENAI_MODEL={model}', content)
        
        with open('.env', 'w') as f:
            f.write(content)
            
        print(f"   {Colors.GREEN}✅ Updated .env to use {model}{Colors.END}")
        
    except Exception as e:
        print(f"   {Colors.YELLOW}⚠️ Could not update .env: {e}{Colors.END}")

def check_api_status():
    """Check OpenAI API status"""
    print(f"\n{Colors.BLUE}📊 Checking API Status{Colors.END}")
    print("-" * 30)
    
    try:
        # Check OpenAI status page
        response = requests.get('https://status.openai.com/api/v2/status.json', timeout=10)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', {}).get('description', 'Unknown')
            print(f"OpenAI Status: {Colors.GREEN}{status}{Colors.END}")
        else:
            print(f"Could not check OpenAI status")
    except:
        print(f"Could not check OpenAI status")

def main():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 60)
    print("🔑 OPENAI API TEST - FREE MODELS")
    print("=" * 60)
    print(f"{Colors.END}")
    
    # Check API status first
    check_api_status()
    
    # Test the API
    if test_openai_free_models():
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 OpenAI API is working!{Colors.END}")
        print(f"{Colors.GREEN}Your Military AI Simulation can now use OpenAI for tactical analysis.{Colors.END}")
        
        # Show next steps
        print(f"\n{Colors.BLUE}🚀 Next Steps:{Colors.END}")
        print("1. Run: python tactical_server.py")
        print("2. Open: http://localhost:8000/tactical-map")
        print("3. Test the AI tactical analysis features")
        
    else:
        print(f"\n{Colors.RED}❌ OpenAI API test failed{Colors.END}")
        print(f"\n{Colors.YELLOW}Possible solutions:{Colors.END}")
        print("1. Wait 1-2 minutes and try again (rate limit)")
        print("2. Check if you have billing set up at https://platform.openai.com/")
        print("3. Verify your API key at https://platform.openai.com/api-keys")
        print("4. Check your usage at https://platform.openai.com/usage")

if __name__ == "__main__":
    main()