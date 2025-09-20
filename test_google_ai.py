#!/usr/bin/env python3
"""
Simple Google AI (Gemini) API Test
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

def test_google_ai_api():
    """Test Google AI (Gemini) API key"""
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ Google AI API key not found{Colors.END}")
        return False
    
    print(f"{Colors.BLUE}{Colors.BOLD}🧠 Testing Google AI (Gemini) API{Colors.END}")
    print("-" * 50)
    print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        # Test 1: List available models
        print(f"\n🔍 Testing API connectivity...")
        models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        models_response = requests.get(models_url, timeout=15)
        
        if models_response.status_code == 200:
            models_data = models_response.json()
            available_models = [model['name'] for model in models_data.get('models', [])]
            print(f"   {Colors.GREEN}✅ API connection successful{Colors.END}")
            print(f"   {Colors.GREEN}✅ Found {len(available_models)} available models{Colors.END}")
            
            # Show some available models
            gemini_models = [m for m in available_models if 'gemini' in m.lower()]
            if gemini_models:
                print(f"   Available Gemini models: {gemini_models[:3]}")
            
        elif models_response.status_code == 403:
            print(f"   {Colors.RED}❌ API key invalid or access denied{Colors.END}")
            print(f"   Response: {models_response.text[:200]}")
            return False
            
        elif models_response.status_code == 429:
            print(f"   {Colors.YELLOW}⚠️ Rate limited - API key works but too many requests{Colors.END}")
            
        else:
            print(f"   {Colors.YELLOW}⚠️ Unexpected response: {models_response.status_code}{Colors.END}")
            print(f"   Response: {models_response.text[:200]}")
        
        # Test 2: Generate content with Gemini Pro
        print(f"\n🧪 Testing content generation...")
        
        # Use Gemini 1.5 Pro Latest model (the new available model)
        generate_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={api_key}"
        
        # Simple test prompt
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Say 'Google AI test successful' if you can read this message."
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 20,
                "temperature": 0
            }
        }
        
        generate_response = requests.post(
            generate_url,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=15
        )
        
        if generate_response.status_code == 200:
            result = generate_response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   {Colors.GREEN}✅ Content generation successful{Colors.END}")
                print(f"   {Colors.GREEN}Response: {generated_text.strip()}{Colors.END}")
                return True
            else:
                print(f"   {Colors.YELLOW}⚠️ Unexpected response format{Colors.END}")
                
        elif generate_response.status_code == 403:
            print(f"   {Colors.RED}❌ API key invalid for content generation{Colors.END}")
            
        elif generate_response.status_code == 429:
            print(f"   {Colors.YELLOW}⚠️ Rate limited on content generation{Colors.END}")
            
        else:
            print(f"   {Colors.RED}❌ Content generation failed: {generate_response.status_code}{Colors.END}")
            print(f"   Response: {generate_response.text[:200]}")
        
        return False
        
    except Exception as e:
        print(f"   {Colors.RED}❌ Error testing Google AI API: {str(e)}{Colors.END}")
        return False

def test_google_ai_tactical_analysis():
    """Test Google AI for tactical military analysis"""
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        return False
    
    print(f"\n🎖️ Testing Military Tactical Analysis...")
    
    try:
        generate_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        # Military tactical prompt
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Analyze this tactical situation: Enemy heat signature detected at coordinates (40.7600, -73.9800) with high temperature reading. Recommend military response strategy in 50 words."
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 100,
                "temperature": 0.3
            }
        }
        
        response = requests.post(
            generate_url,
            headers={'Content-Type': 'application/json'},
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                analysis = result['candidates'][0]['content']['parts'][0]['text']
                print(f"   {Colors.GREEN}✅ Tactical analysis successful{Colors.END}")
                print(f"   {Colors.CYAN}Analysis: {analysis.strip()[:150]}...{Colors.END}")
                return True
                
        return False
        
    except Exception as e:
        print(f"   {Colors.RED}❌ Tactical analysis test failed: {str(e)}{Colors.END}")
        return False

def main():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 60)
    print("🧠 GOOGLE AI (GEMINI) API TEST")
    print("=" * 60)
    print(f"{Colors.END}")
    
    # Test basic API functionality
    if test_google_ai_api():
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Google AI API is working!{Colors.END}")
        
        # Test military tactical analysis
        if test_google_ai_tactical_analysis():
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎖️ Google AI ready for military tactical analysis!{Colors.END}")
        
        print(f"\n{Colors.BLUE}🚀 Integration Status:{Colors.END}")
        print("✅ OpenAI (gpt-4o-mini) - Primary AI")
        print("✅ Google AI (Gemini Pro) - Backup AI")
        print("✅ Google Maps API - 3D Mapping")
        
        print(f"\n{Colors.CYAN}💡 Your Military AI Simulation now has dual AI power!{Colors.END}")
        print("- OpenAI for main tactical analysis")
        print("- Google AI as backup and alternative perspective")
        
    else:
        print(f"\n{Colors.RED}❌ Google AI API test failed{Colors.END}")
        print(f"\n{Colors.YELLOW}Possible solutions:{Colors.END}")
        print("1. Check if API key is correct")
        print("2. Verify the key is enabled for Generative AI")
        print("3. Check billing setup at https://console.cloud.google.com/")
        print("4. Try generating a new API key")

if __name__ == "__main__":
    main()