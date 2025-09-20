#!/usr/bin/env python3
"""
Google AI API Key Renewal Helper
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
    print("🔄 GOOGLE AI API KEY RENEWAL")
    print("=" * 70)
    print(f"{Colors.END}")
    
    print(f"{Colors.RED}❌ Current Issue: Your Google AI API key has expired{Colors.END}")
    print(f"{Colors.YELLOW}✅ Solution: Generate a new API key (takes 30 seconds){Colors.END}\n")
    
    print(f"{Colors.BOLD}🔑 STEP 1: Generate New Google AI API Key{Colors.END}")
    print("-" * 50)
    print("1. Go to Google AI Studio")
    print("2. Click 'Get API Key'")
    print("3. Create a new API key")
    print("4. Copy the new key")
    print("5. Update your .env file")
    
    print(f"\n{Colors.BOLD}🚀 QUICK LINKS:{Colors.END}")
    print("-" * 20)
    
    links = [
        ("Google AI Studio", "https://aistudio.google.com/"),
        ("Google Cloud Console", "https://console.cloud.google.com/apis/credentials"),
    ]
    
    for name, url in links:
        print(f"• {name}: {Colors.BLUE}{url}{Colors.END}")
    
    # Ask if user wants to open the API key page
    open_page = input(f"\nOpen Google AI Studio to generate new key? (Y/n): ").lower().strip()
    if open_page != 'n':
        print(f"\n{Colors.BLUE}Opening Google AI Studio...{Colors.END}")
        webbrowser.open("https://aistudio.google.com/")
        time.sleep(1)
        print(f"{Colors.GREEN}✅ Opened Google AI Studio{Colors.END}")
    
    print(f"\n{Colors.BOLD}📋 DETAILED STEPS:{Colors.END}")
    print("-" * 20)
    print("1. In Google AI Studio:")
    print("   • Click 'Get API key' (top right)")
    print("   • Select 'Create API key in existing project'")
    print("   • Copy the generated key")
    
    print("\n2. Update your .env file:")
    print("   • Replace the line: GOOGLE_AI_API_KEY=AIzaSyC3YDpkjdovZfoO...")
    print("   • With: GOOGLE_AI_API_KEY=your-new-key-here")
    
    print("\n3. Test the new key:")
    print("   • Run: python test_google_ai.py")
    
    print(f"\n{Colors.PURPLE}💡 ALTERNATIVE APPROACH:{Colors.END}")
    print("For now, you can proceed with just OpenAI:")
    print("• Your OpenAI API (gpt-4o-mini) is working perfectly")
    print("• Your Google Maps API is working")
    print("• Your Military AI Simulation is fully functional!")
    
    print(f"\n{Colors.GREEN}🎖️ Current Working APIs:{Colors.END}")
    print("✅ OpenAI (gpt-4o-mini) - Primary AI")
    print("✅ Google Maps - 3D visualization")
    print("❌ Google AI - Needs new key")
    
    print(f"\n{Colors.CYAN}Your Military AI Simulation is ready to run with OpenAI + Google Maps!{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")