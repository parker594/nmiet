#!/usr/bin/env python3
"""
Comprehensive API Key Verification
"""

import os
import requests
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

def test_api_key(name, key, test_func):
    """Test an API key with the provided test function"""
    if not key or key.startswith('your-') or key == 'DEMO_KEY':
        print(f"   {Colors.YELLOW}⚠️ {name}: NOT CONFIGURED{Colors.END}")
        return False
    
    try:
        result = test_func(key)
        if result:
            print(f"   {Colors.GREEN}✅ {name}: WORKING{Colors.END}")
            return True
        else:
            print(f"   {Colors.RED}❌ {name}: FAILED{Colors.END}")
            return False
    except Exception as e:
        print(f"   {Colors.RED}❌ {name}: ERROR - {str(e)[:50]}{Colors.END}")
        return False

def test_openai(key):
    """Test OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        return True
    except Exception as e:
        if "quota" in str(e).lower():
            return True  # Key is valid, just out of quota
        return False

def test_google_ai(key):
    """Test Google AI API"""
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def test_google_maps(key):
    """Test Google Maps API"""
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key={key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get('status') == 'OK'
    except:
        return False

def test_openweather(key):
    """Test OpenWeatherMap API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={key}"
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def test_nasa(key):
    """Test NASA API"""
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={key}"
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    """Test all configured API keys"""
    
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("🔑 API KEY VERIFICATION SYSTEM")
    print("=" * 60)
    print(f"{Colors.END}")
    
    # Test essential APIs
    print(f"{Colors.CYAN}🤖 ESSENTIAL AI APIS{Colors.END}")
    print("-" * 40)
    
    openai_key = os.getenv('OPENAI_API_KEY')
    google_ai_key = os.getenv('GOOGLE_AI_API_KEY')
    
    working_count = 0
    total_count = 0
    
    # Test OpenAI
    total_count += 1
    if test_api_key("OpenAI GPT-4o-mini", openai_key, test_openai):
        working_count += 1
    
    # Test Google AI
    total_count += 1
    if test_api_key("Google AI/Gemini", google_ai_key, test_google_ai):
        working_count += 1
    
    print(f"\n{Colors.CYAN}🗺️ MAPPING APIS{Colors.END}")
    print("-" * 40)
    
    # Test Google Maps
    google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY')
    total_count += 1
    if test_api_key("Google Maps", google_maps_key, test_google_maps):
        working_count += 1
    
    print(f"\n{Colors.CYAN}🌤️ WEATHER APIS{Colors.END}")
    print("-" * 40)
    
    # Test OpenWeatherMap
    openweather_key = os.getenv('OPENWEATHER_API_KEY')
    total_count += 1
    if test_api_key("OpenWeatherMap", openweather_key, test_openweather):
        working_count += 1
    
    # Test NASA
    nasa_key = os.getenv('NASA_API_KEY')
    total_count += 1
    if test_api_key("NASA", nasa_key, test_nasa):
        working_count += 1
    
    print(f"\n{Colors.CYAN}📊 CONFIGURED BUT NOT TESTED{Colors.END}")
    print("-" * 40)
    
    # List other configured keys
    other_keys = [
        ('AccuWeather', os.getenv('ACCUWEATHER_API_KEY')),
        ('Planet Labs', os.getenv('PLANET_API_KEY')),
        ('Sentinel Hub', os.getenv('SENTINEL_HUB_CLIENT_ID')),
    ]
    
    for name, key in other_keys:
        if key and not key.startswith('your-'):
            print(f"   {Colors.BLUE}ℹ️ {name}: CONFIGURED{Colors.END}")
        else:
            print(f"   {Colors.YELLOW}⚠️ {name}: NOT SET{Colors.END}")
    
    # Summary
    print(f"\n{Colors.BOLD}=" * 60)
    print(f"📊 SUMMARY: {working_count}/{total_count} ESSENTIAL APIs WORKING")
    
    if working_count >= 3:
        print(f"{Colors.GREEN}🎯 EXCELLENT! Your military AI simulation is ready!{Colors.END}")
    elif working_count >= 2:
        print(f"{Colors.YELLOW}⚠️ GOOD! Most features will work.{Colors.END}")
    else:
        print(f"{Colors.RED}❌ WARNING! Need more working APIs for full functionality.{Colors.END}")
    
    print("=" * 60)
    print(f"{Colors.END}")

if __name__ == "__main__":
    main()