#!/usr/bin/env python3
"""
API Keys Testing Script for Military AI Simulation Platform
This script tests all configured API keys to ensure they're working correctly.
"""

import os
import sys
import requests
import json
from datetime import datetime
import time

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    """Print the test header"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("="*70)
    print("🔑 MILITARY AI SIMULATION - API KEYS TEST SUITE")
    print("="*70)
    print(f"{Colors.END}")
    print(f"{Colors.YELLOW}Testing all configured API keys...{Colors.END}\n")

def test_openai_api():
    """Test OpenAI API key"""
    print(f"{Colors.BLUE}🤖 Testing OpenAI API...{Colors.END}")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ OpenAI API key not found in environment{Colors.END}")
        return False
    
    if not api_key.startswith('sk-'):
        print(f"{Colors.RED}❌ Invalid OpenAI API key format{Colors.END}")
        return False
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple completion request
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': 'Test'}],
            'max_tokens': 5
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ OpenAI API key is valid and working{Colors.END}")
            return True
        elif response.status_code == 401:
            print(f"{Colors.RED}❌ OpenAI API key is invalid{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ OpenAI API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing OpenAI API: {str(e)}{Colors.END}")
        return False

def test_google_ai_api():
    """Test Google AI API key"""
    print(f"{Colors.BLUE}🧠 Testing Google AI API...{Colors.END}")
    
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ Google AI API key not found in environment{Colors.END}")
        return False
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ Google AI API key is valid and working{Colors.END}")
            return True
        elif response.status_code == 403:
            print(f"{Colors.RED}❌ Google AI API key is invalid or access denied{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ Google AI API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing Google AI API: {str(e)}{Colors.END}")
        return False

def test_huggingface_api():
    """Test Hugging Face API key"""
    print(f"{Colors.BLUE}🤗 Testing Hugging Face API...{Colors.END}")
    
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ Hugging Face API key not found in environment{Colors.END}")
        return False
    
    if not api_key.startswith('hf_'):
        print(f"{Colors.RED}❌ Invalid Hugging Face API key format{Colors.END}")
        return False
    
    try:
        headers = {'Authorization': f'Bearer {api_key}'}
        url = "https://huggingface.co/api/whoami"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"{Colors.GREEN}✅ Hugging Face API key is valid - User: {user_info.get('name', 'Unknown')}{Colors.END}")
            return True
        elif response.status_code == 401:
            print(f"{Colors.RED}❌ Hugging Face API key is invalid{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ Hugging Face API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing Hugging Face API: {str(e)}{Colors.END}")
        return False

def test_google_maps_api():
    """Test Google Maps API key with multiple APIs"""
    print(f"{Colors.BLUE}🗺️ Testing Google Maps APIs...{Colors.END}")
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ Google Maps API key not found in environment{Colors.END}")
        return False
    
    # Test multiple Google Maps APIs
    tests = [
        ("Geocoding API", f"https://maps.googleapis.com/maps/api/geocode/json?address=Pentagon,Arlington,VA&key={api_key}"),
        ("Directions API", f"https://maps.googleapis.com/maps/api/directions/json?origin=Pentagon,Arlington,VA&destination=White+House,Washington,DC&key={api_key}"),
        ("Places API", f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=military+base+washington&key={api_key}"),
    ]
    
    successful_tests = 0
    total_tests = len(tests)
    
    try:
        for test_name, url in tests:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' or 'results' in data:
                    print(f"  ✅ {test_name}: Working")
                    successful_tests += 1
                elif data.get('status') == 'REQUEST_DENIED':
                    print(f"  ❌ {test_name}: API not enabled or key restricted")
                elif data.get('status') == 'OVER_QUERY_LIMIT':
                    print(f"  ⚠️ {test_name}: Rate limit exceeded")
                else:
                    print(f"  ⚠️ {test_name}: Status - {data.get('status', 'Unknown')}")
            else:
                print(f"  ❌ {test_name}: HTTP {response.status_code}")
        
        if successful_tests == total_tests:
            print(f"{Colors.GREEN}✅ All Google Maps APIs working ({successful_tests}/{total_tests}){Colors.END}")
            return True
        elif successful_tests > 0:
            print(f"{Colors.YELLOW}⚠️ Partial success ({successful_tests}/{total_tests}) - Enable missing APIs in Google Cloud Console{Colors.END}")
            return False
        else:
            print(f"{Colors.RED}❌ Google Maps API key is invalid or no APIs enabled{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing Google Maps APIs: {str(e)}{Colors.END}")
        return False

def test_openweather_api():
    """Test OpenWeatherMap API key"""
    print(f"{Colors.BLUE}🌤️ Testing OpenWeatherMap API...{Colors.END}")
    
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print(f"{Colors.RED}❌ OpenWeatherMap API key not found in environment{Colors.END}")
        return False
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"{Colors.GREEN}✅ OpenWeatherMap API key is valid - Current temp in London: {data['main']['temp']}K{Colors.END}")
            return True
        elif response.status_code == 401:
            print(f"{Colors.RED}❌ OpenWeatherMap API key is invalid{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ OpenWeatherMap API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing OpenWeatherMap API: {str(e)}{Colors.END}")
        return False

def test_nasa_api():
    """Test NASA API key"""
    print(f"{Colors.BLUE}🚀 Testing NASA API...{Colors.END}")
    
    api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if api_key == 'DEMO_KEY':
                print(f"{Colors.GREEN}✅ NASA API working with DEMO_KEY - Title: {data.get('title', 'Unknown')}{Colors.END}")
            else:
                print(f"{Colors.GREEN}✅ NASA API key is valid - Title: {data.get('title', 'Unknown')}{Colors.END}")
            return True
        elif response.status_code == 403:
            print(f"{Colors.RED}❌ NASA API key is invalid or rate limited{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ NASA API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing NASA API: {str(e)}{Colors.END}")
        return False

def test_mapbox_api():
    """Test Mapbox API key"""
    print(f"{Colors.BLUE}🗺️ Testing Mapbox API...{Colors.END}")
    
    api_key = os.getenv('MAPBOX_ACCESS_TOKEN')
    if not api_key:
        print(f"{Colors.RED}❌ Mapbox access token not found in environment{Colors.END}")
        return False
    
    try:
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/Los%20Angeles.json?access_token={api_key}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'features' in data and len(data['features']) > 0:
                print(f"{Colors.GREEN}✅ Mapbox API key is valid and working{Colors.END}")
                return True
            else:
                print(f"{Colors.YELLOW}⚠️ Mapbox API returned no results{Colors.END}")
                return False
        elif response.status_code == 401:
            print(f"{Colors.RED}❌ Mapbox API key is invalid{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ Mapbox API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing Mapbox API: {str(e)}{Colors.END}")
        return False

def test_azure_cognitive_api():
    """Test Azure Cognitive Services API key"""
    print(f"{Colors.BLUE}🧠 Testing Azure Cognitive Services API...{Colors.END}")
    
    api_key = os.getenv('AZURE_COGNITIVE_KEY')
    endpoint = os.getenv('AZURE_COGNITIVE_ENDPOINT')
    
    if not api_key:
        print(f"{Colors.RED}❌ Azure Cognitive Services API key not found in environment{Colors.END}")
        return False
    
    if not endpoint:
        print(f"{Colors.RED}❌ Azure Cognitive Services endpoint not found in environment{Colors.END}")
        return False
    
    try:
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/json'
        }
        
        # Test with text analytics (sentiment analysis)
        url = f"{endpoint}/text/analytics/v3.1/sentiment"
        data = {
            "documents": [
                {"id": "1", "text": "This is a test message.", "language": "en"}
            ]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            print(f"{Colors.GREEN}✅ Azure Cognitive Services API key is valid and working{Colors.END}")
            return True
        elif response.status_code == 401:
            print(f"{Colors.RED}❌ Azure Cognitive Services API key is invalid{Colors.END}")
            return False
        elif response.status_code == 404:
            print(f"{Colors.YELLOW}⚠️ Azure endpoint URL might be incorrect{Colors.END}")
            return False
        else:
            print(f"{Colors.YELLOW}⚠️ Azure Cognitive Services API responded with status {response.status_code}{Colors.END}")
            return False
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error testing Azure Cognitive Services API: {str(e)}{Colors.END}")
        return False

def main():
    """Main function to run all API tests"""
    print_header()
    
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print(f"{Colors.GREEN}✅ Loaded environment variables from .env file{Colors.END}\n")
    except ImportError:
        print(f"{Colors.YELLOW}⚠️ python-dotenv not installed. Using system environment variables.{Colors.END}\n")
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️ Could not load .env file: {str(e)}{Colors.END}\n")
    
    # List of test functions
    tests = [
        ("OpenAI API", test_openai_api),
        ("Google AI API", test_google_ai_api),
        ("Hugging Face API", test_huggingface_api),
        ("Google Maps API", test_google_maps_api),
        ("OpenWeatherMap API", test_openweather_api),
        ("NASA API", test_nasa_api),
        ("Mapbox API", test_mapbox_api),
        ("Azure Cognitive Services", test_azure_cognitive_api),
    ]
    
    passed = 0
    total = len(tests)
    
    # Run all tests
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            print()  # Add spacing between tests
            time.sleep(0.5)  # Brief pause between tests
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
            break
        except Exception as e:
            print(f"{Colors.RED}❌ Unexpected error in {test_name}: {str(e)}{Colors.END}\n")
    
    # Print results summary
    print("="*70)
    print(f"{Colors.BOLD}📊 TEST RESULTS SUMMARY{Colors.END}")
    print("="*70)
    
    if passed == total:
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! ({passed}/{total}){Colors.END}")
        print(f"{Colors.GREEN}✅ Your Military AI Simulation Platform is ready for deployment!{Colors.END}")
    elif passed > total // 2:
        print(f"{Colors.YELLOW}⚠️ PARTIAL SUCCESS ({passed}/{total} tests passed){Colors.END}")
        print(f"{Colors.YELLOW}Some APIs are working. You can start development with available services.{Colors.END}")
    else:
        print(f"{Colors.RED}❌ MOST TESTS FAILED ({passed}/{total} tests passed){Colors.END}")
        print(f"{Colors.RED}Please check your API keys and network connection.{Colors.END}")
    
    print(f"\n{Colors.CYAN}💡 Tip: Check the API_KEYS_GUIDE.md file for detailed setup instructions.{Colors.END}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)