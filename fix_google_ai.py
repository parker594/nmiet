#!/usr/bin/env python3
"""
Google AI API Setup Helper - Enable Required APIs
"""

import webbrowser
import time

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def main():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("🔧 GOOGLE AI API SETUP - ENABLE REQUIRED APIS")
    print("=" * 70)
    print(f"{Colors.END}")
    
    print(f"{Colors.YELLOW}Your Google AI API key is valid, but the APIs need to be enabled!{Colors.END}\n")
    
    apis_to_enable = [
        {
            "name": "Generative Language API (Gemini)",
            "url": "https://console.developers.google.com/apis/library/generativelanguage.googleapis.com",
            "description": "Required for Google AI/Gemini text generation"
        },
        {
            "name": "AI Platform API", 
            "url": "https://console.developers.google.com/apis/library/aiplatform.googleapis.com",
            "description": "Optional - for advanced AI features"
        }
    ]
    
    print(f"{Colors.BOLD}🎯 STEP 1: Enable Required Google APIs{Colors.END}")
    print("-" * 50)
    
    for i, api in enumerate(apis_to_enable, 1):
        print(f"{Colors.GREEN}{i}. {api['name']}{Colors.END}")
        print(f"   Purpose: {api['description']}")
        print(f"   URL: {Colors.BLUE}{api['url']}{Colors.END}")
        print()
    
    # Ask if user wants to open these URLs
    open_apis = input(f"Open API enable pages in browser? (Y/n): ").lower().strip()
    if open_apis != 'n':
        print(f"\n{Colors.BLUE}Opening API enable pages...{Colors.END}")
        for api in apis_to_enable:
            webbrowser.open(api['url'])
            time.sleep(2)  # Brief delay between opens
        print(f"{Colors.GREEN}✅ Opened all API enable pages{Colors.END}")
    
    print(f"\n{Colors.BOLD}📋 MANUAL STEPS TO COMPLETE:{Colors.END}")
    print("-" * 50)
    print("1. Click 'ENABLE' on each API page that opened")
    print("2. Wait 1-2 minutes for APIs to activate")
    print("3. Run the test again: python test_google_ai.py")
    
    print(f"\n{Colors.BOLD}🔍 ALTERNATIVE METHOD:{Colors.END}")
    print("-" * 50)
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Select your project")
    print("3. Navigate to: APIs & Services > Library")
    print("4. Search for: 'Generative Language API'")
    print("5. Click on it and click 'ENABLE'")
    
    print(f"\n{Colors.PURPLE}💡 IMPORTANT NOTES:{Colors.END}")
    print("• Your API key is correct and valid")
    print("• You just need to enable the Generative Language API")
    print("• This is a one-time setup step")
    print("• The API should activate within 1-2 minutes")
    
    print(f"\n{Colors.CYAN}🎖️ After enabling, your Military AI will have dual AI power!{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")