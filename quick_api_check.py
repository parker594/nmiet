#!/usr/bin/env python3
"""
Quick API Key Check
"""

import os
import sys

# Set environment variables directly from .env file
def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
                    os.environ[key] = value
    except FileNotFoundError:
        print("❌ .env file not found")
        return env_vars
    return env_vars

def main():
    print("🔑 API KEY STATUS CHECK")
    print("=" * 50)
    
    env_vars = load_env()
    
    # Check essential API keys
    essential_keys = {
        'OpenAI API': 'OPENAI_API_KEY',
        'Google AI': 'GOOGLE_AI_API_KEY', 
        'Google Maps': 'GOOGLE_MAPS_API_KEY',
        'OpenWeather': 'OPENWEATHER_API_KEY',
        'NASA': 'NASA_API_KEY'
    }
    
    print("\n🤖 ESSENTIAL APIs:")
    working = 0
    
    for name, key in essential_keys.items():
        value = env_vars.get(key, '')
        if value and not value.startswith('your-') and len(value) > 10:
            print(f"   ✅ {name}: CONFIGURED ({value[:20]}...)")
            working += 1
        else:
            print(f"   ❌ {name}: NOT SET")
    
    print("\n📊 ADDITIONAL APIs:")
    additional_keys = {
        'AccuWeather': 'ACCUWEATHER_API_KEY',
        'Planet Labs': 'PLANET_API_KEY',
        'Sentinel Hub': 'SENTINEL_HUB_CLIENT_ID'
    }
    
    for name, key in additional_keys.items():
        value = env_vars.get(key, '')
        if value and not value.startswith('your-') and len(value) > 10:
            print(f"   ✅ {name}: CONFIGURED")
        else:
            print(f"   ⚠️ {name}: NOT SET")
    
    print(f"\n🎯 RESULT: {working}/{len(essential_keys)} essential APIs configured")
    
    if working >= 4:
        print("🚀 EXCELLENT! Your simulation is fully ready!")
    elif working >= 3:
        print("👍 GOOD! Most features will work perfectly!")
    elif working >= 2:
        print("⚠️ OK! Basic functionality available!")
    else:
        print("❌ WARNING! Need more APIs for full functionality!")

if __name__ == "__main__":
    main()