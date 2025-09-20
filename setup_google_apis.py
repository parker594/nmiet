#!/usr/bin/env python3
"""
Google Cloud API Setup Helper
This script provides the exact links and commands to enable Google Cloud APIs
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

def print_header():
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("="*70)
    print("🗺️ GOOGLE CLOUD APIs SETUP HELPER")
    print("="*70)
    print(f"{Colors.END}")

def main():
    print_header()
    
    print(f"{Colors.YELLOW}This script will help you enable the required Google Cloud APIs{Colors.END}")
    print(f"{Colors.YELLOW}for your Military AI Simulation Platform.{Colors.END}\n")
    
    # Essential APIs
    essential_apis = [
        {
            "name": "Maps JavaScript API",
            "purpose": "3D map rendering in browser",
            "url": "https://console.cloud.google.com/apis/library/maps-backend.googleapis.com",
            "priority": "ESSENTIAL"
        },
        {
            "name": "Places API", 
            "purpose": "Location search and geocoding",
            "url": "https://console.cloud.google.com/apis/library/places-backend.googleapis.com",
            "priority": "ESSENTIAL"
        },
        {
            "name": "Geocoding API",
            "purpose": "Address to coordinates conversion", 
            "url": "https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com",
            "priority": "ESSENTIAL"
        },
        {
            "name": "Directions API",
            "purpose": "Route planning and navigation",
            "url": "https://console.cloud.google.com/apis/library/directions-backend.googleapis.com", 
            "priority": "ESSENTIAL"
        }
    ]
    
    # Recommended APIs
    recommended_apis = [
        {
            "name": "Maps Static API",
            "purpose": "Static map images for reports",
            "url": "https://console.cloud.google.com/apis/library/static-maps-backend.googleapis.com",
            "priority": "RECOMMENDED"
        },
        {
            "name": "Street View Static API",
            "purpose": "Ground-level reconnaissance",
            "url": "https://console.cloud.google.com/apis/library/street-view-image-backend.googleapis.com",
            "priority": "RECOMMENDED"
        },
        {
            "name": "Earth Engine API",
            "purpose": "Satellite imagery and analysis",
            "url": "https://console.cloud.google.com/apis/library/earthengine.googleapis.com",
            "priority": "RECOMMENDED"
        }
    ]
    
    print(f"{Colors.BOLD}🎯 STEP 1: Enable Essential APIs{Colors.END}")
    print("-" * 50)
    
    for i, api in enumerate(essential_apis, 1):
        print(f"{Colors.GREEN}{i}. {api['name']}{Colors.END}")
        print(f"   Purpose: {api['purpose']}")
        print(f"   URL: {Colors.BLUE}{api['url']}{Colors.END}")
        print()
    
    # Ask if user wants to open these URLs
    open_essential = input(f"Open essential API pages in browser? (Y/n): ").lower().strip()
    if open_essential != 'n':
        print(f"\n{Colors.BLUE}Opening essential APIs...{Colors.END}")
        for api in essential_apis:
            webbrowser.open(api['url'])
            time.sleep(2)  # Brief delay between opens
        print(f"{Colors.GREEN}✅ Opened all essential API pages{Colors.END}")
    
    print(f"\n{Colors.BOLD}⭐ STEP 2: Enable Recommended APIs{Colors.END}")
    print("-" * 50)
    
    for i, api in enumerate(recommended_apis, 1):
        print(f"{Colors.YELLOW}{i}. {api['name']}{Colors.END}")
        print(f"   Purpose: {api['purpose']}")
        print(f"   URL: {Colors.BLUE}{api['url']}{Colors.END}")
        print()
    
    open_recommended = input(f"Open recommended API pages in browser? (y/N): ").lower().strip()
    if open_recommended == 'y':
        print(f"\n{Colors.BLUE}Opening recommended APIs...{Colors.END}")
        for api in recommended_apis:
            webbrowser.open(api['url'])
            time.sleep(2)
        print(f"{Colors.GREEN}✅ Opened all recommended API pages{Colors.END}")
    
    # API Key Creation
    print(f"\n{Colors.BOLD}🔑 STEP 3: Create and Secure API Key{Colors.END}")
    print("-" * 50)
    
    print("1. Go to: APIs & Services > Credentials")
    print("2. Click 'Create Credentials' > 'API Key'")
    print("3. Copy the generated key")
    print("4. IMMEDIATELY click 'Restrict Key'")
    print("5. Set application restrictions (HTTP referrers for frontend, IP for backend)")
    print("6. Select only the APIs you enabled")
    print("7. Save the restrictions")
    
    open_credentials = input(f"\nOpen Google Cloud Credentials page? (Y/n): ").lower().strip()
    if open_credentials != 'n':
        webbrowser.open("https://console.cloud.google.com/apis/credentials")
        print(f"{Colors.GREEN}✅ Opened Google Cloud Credentials page{Colors.END}")
    
    # Testing
    print(f"\n{Colors.BOLD}🧪 STEP 4: Test Your Setup{Colors.END}")
    print("-" * 50)
    
    print("After creating your API key:")
    print(f"1. Update your .env file: {Colors.CYAN}GOOGLE_MAPS_API_KEY=your-key-here{Colors.END}")
    print(f"2. Run: {Colors.CYAN}python test_api_keys.py{Colors.END}")
    print(f"3. Look for: {Colors.GREEN}✅ All Google Maps APIs working (4/4){Colors.END}")
    
    # Quick reference
    print(f"\n{Colors.BOLD}📋 QUICK REFERENCE{Colors.END}")
    print("-" * 50)
    print(f"{Colors.GREEN}Essential for your Military AI:{Colors.END}")
    print("• Maps JavaScript API - 3D tactical map")
    print("• Geocoding API - Address/coordinate conversion")
    print("• Directions API - Route planning")
    print("• Places API - Location search")
    
    print(f"\n{Colors.YELLOW}Recommended for advanced features:{Colors.END}")
    print("• Maps Static API - Report generation")
    print("• Street View Static API - Ground reconnaissance")
    print("• Earth Engine API - Satellite imagery")
    
    print(f"\n{Colors.PURPLE}💰 Cost (with $200 free credit):{Colors.END}")
    print("• Maps JavaScript: ~28k map loads/month")
    print("• Geocoding: ~40k requests/month")
    print("• Directions: ~40k requests/month")
    print("• Places: ~11k requests/month")
    
    print(f"\n{Colors.CYAN}🎖️ Ready to enable your Google Cloud APIs for military operations!{Colors.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}")