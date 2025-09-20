#!/usr/bin/env python3
"""
Environment Setup Helper for Military AI Simulation Platform
This script helps you set up your .env file interactively.
"""

import os
import sys
from pathlib import Path

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
    """Print the setup header"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("="*70)
    print("🔧 MILITARY AI SIMULATION - ENVIRONMENT SETUP")
    print("="*70)
    print(f"{Colors.END}")
    print(f"{Colors.YELLOW}This script will help you set up your .env file with API keys.{Colors.END}\n")

def get_user_input(prompt, description="", optional=False, current_value=""):
    """Get user input with helpful prompts"""
    if description:
        print(f"{Colors.BLUE}ℹ️  {description}{Colors.END}")
    
    if current_value:
        prompt += f" (current: {current_value[:20]}...)" if len(current_value) > 20 else f" (current: {current_value})"
    
    if optional:
        prompt += f" {Colors.YELLOW}[OPTIONAL]{Colors.END}"
    
    prompt += ": "
    
    try:
        value = input(prompt).strip()
        if not value and current_value:
            return current_value
        return value
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
        sys.exit(0)

def load_existing_env():
    """Load existing .env file if it exists"""
    env_file = Path('.env')
    env_vars = {}
    
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip().strip('"\'')
            print(f"{Colors.GREEN}✅ Found existing .env file with {len(env_vars)} variables{Colors.END}\n")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️ Could not read existing .env file: {e}{Colors.END}\n")
    
    return env_vars

def save_env_file(env_vars):
    """Save environment variables to .env file"""
    try:
        with open('.env', 'w') as f:
            f.write("# Military AI Simulation Platform - Environment Variables\n")
            f.write(f"# Generated on: {os.popen('date').read().strip()}\n\n")
            
            # AI Model APIs
            f.write("# =============================================================================\n")
            f.write("# AI MODEL APIs\n")
            f.write("# =============================================================================\n\n")
            
            ai_keys = [
                'OPENAI_API_KEY',
                'GOOGLE_AI_API_KEY', 
                'HUGGINGFACE_API_KEY',
                'AZURE_COGNITIVE_KEY',
                'AZURE_COGNITIVE_ENDPOINT'
            ]
            
            for key in ai_keys:
                value = env_vars.get(key, '')
                f.write(f"{key}={value}\n")
            
            # Mapping APIs
            f.write("\n# =============================================================================\n")
            f.write("# MAPPING & GEOSPATIAL APIs\n")
            f.write("# =============================================================================\n\n")
            
            map_keys = [
                'GOOGLE_MAPS_API_KEY',
                'MAPBOX_ACCESS_TOKEN',
                'NASA_API_KEY'
            ]
            
            for key in map_keys:
                value = env_vars.get(key, '')
                f.write(f"{key}={value}\n")
            
            # Weather APIs
            f.write("\n# =============================================================================\n")
            f.write("# WEATHER APIs\n")
            f.write("# =============================================================================\n\n")
            
            weather_keys = [
                'OPENWEATHER_API_KEY',
                'ACCUWEATHER_API_KEY'
            ]
            
            for key in weather_keys:
                value = env_vars.get(key, '')
                f.write(f"{key}={value}\n")
            
            # Optional APIs
            f.write("\n# =============================================================================\n")
            f.write("# OPTIONAL APIs\n")
            f.write("# =============================================================================\n\n")
            
            optional_keys = [
                'AWS_ACCESS_KEY_ID',
                'AWS_SECRET_ACCESS_KEY',
                'AUTH0_DOMAIN',
                'AUTH0_CLIENT_ID',
                'AUTH0_CLIENT_SECRET'
            ]
            
            for key in optional_keys:
                value = env_vars.get(key, '')
                f.write(f"{key}={value}\n")
        
        print(f"{Colors.GREEN}✅ Successfully saved .env file!{Colors.END}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error saving .env file: {e}{Colors.END}")
        return False

def main():
    """Main setup function"""
    print_header()
    
    # Load existing environment variables
    env_vars = load_existing_env()
    
    print(f"{Colors.PURPLE}Let's set up your API keys step by step.{Colors.END}")
    print(f"{Colors.PURPLE}Press Enter to skip optional fields or keep existing values.{Colors.END}\n")
    
    # AI Model APIs (Priority)
    print(f"{Colors.BOLD}🤖 AI MODEL APIs (High Priority){Colors.END}")
    print("-" * 50)
    
    env_vars['OPENAI_API_KEY'] = get_user_input(
        "OpenAI API Key",
        "Get from: https://platform.openai.com/api-keys (starts with 'sk-')",
        current_value=env_vars.get('OPENAI_API_KEY', '')
    )
    
    env_vars['GOOGLE_AI_API_KEY'] = get_user_input(
        "Google AI API Key",
        "Get from: https://aistudio.google.com/ (for Gemini Pro)",
        current_value=env_vars.get('GOOGLE_AI_API_KEY', '')
    )
    
    env_vars['HUGGINGFACE_API_KEY'] = get_user_input(
        "Hugging Face API Key",
        "Get from: https://huggingface.co/settings/tokens (starts with 'hf_')",
        current_value=env_vars.get('HUGGINGFACE_API_KEY', '')
    )
    
    print(f"\n{Colors.BOLD}🗺️ MAPPING APIs (High Priority){Colors.END}")
    print("-" * 50)
    
    env_vars['GOOGLE_MAPS_API_KEY'] = get_user_input(
        "Google Maps API Key",
        "Get from: https://console.cloud.google.com/ (enable Maps JavaScript API)",
        current_value=env_vars.get('GOOGLE_MAPS_API_KEY', '')
    )
    
    env_vars['MAPBOX_ACCESS_TOKEN'] = get_user_input(
        "Mapbox Access Token",
        "Get from: https://account.mapbox.com/ (public token starts with 'pk.')",
        optional=True,
        current_value=env_vars.get('MAPBOX_ACCESS_TOKEN', '')
    )
    
    print(f"\n{Colors.BOLD}🌤️ WEATHER APIs (Medium Priority){Colors.END}")
    print("-" * 50)
    
    env_vars['OPENWEATHER_API_KEY'] = get_user_input(
        "OpenWeatherMap API Key",
        "Get from: https://openweathermap.org/api (free tier: 1000 calls/day)",
        current_value=env_vars.get('OPENWEATHER_API_KEY', '')
    )
    
    env_vars['NASA_API_KEY'] = get_user_input(
        "NASA API Key",
        "Get from: https://api.nasa.gov/ (leave empty to use DEMO_KEY)",
        optional=True,
        current_value=env_vars.get('NASA_API_KEY', 'DEMO_KEY')
    )
    
    if not env_vars['NASA_API_KEY']:
        env_vars['NASA_API_KEY'] = 'DEMO_KEY'
    
    # Ask about Azure (more complex setup)
    print(f"\n{Colors.BOLD}🧠 AZURE COGNITIVE SERVICES (Optional){Colors.END}")
    print("-" * 50)
    
    setup_azure = input(f"Set up Azure Cognitive Services? (y/N): ").lower().strip()
    if setup_azure == 'y':
        env_vars['AZURE_COGNITIVE_KEY'] = get_user_input(
            "Azure Cognitive Services API Key",
            "Get from: https://portal.azure.com/ (create Cognitive Services resource)",
            current_value=env_vars.get('AZURE_COGNITIVE_KEY', '')
        )
        
        env_vars['AZURE_COGNITIVE_ENDPOINT'] = get_user_input(
            "Azure Cognitive Services Endpoint",
            "Format: https://your-region.cognitiveservices.azure.com/",
            current_value=env_vars.get('AZURE_COGNITIVE_ENDPOINT', '')
        )
    
    # Optional APIs
    print(f"\n{Colors.BOLD}⚙️ OPTIONAL APIs{Colors.END}")
    print("-" * 50)
    
    setup_optional = input(f"Set up additional optional APIs (AWS, Auth0)? (y/N): ").lower().strip()
    if setup_optional == 'y':
        env_vars['ACCUWEATHER_API_KEY'] = get_user_input(
            "AccuWeather API Key",
            "Get from: https://developer.accuweather.com/",
            optional=True,
            current_value=env_vars.get('ACCUWEATHER_API_KEY', '')
        )
        
        env_vars['AWS_ACCESS_KEY_ID'] = get_user_input(
            "AWS Access Key ID",
            "Get from: https://console.aws.amazon.com/iam/",
            optional=True,
            current_value=env_vars.get('AWS_ACCESS_KEY_ID', '')
        )
        
        if env_vars['AWS_ACCESS_KEY_ID']:
            env_vars['AWS_SECRET_ACCESS_KEY'] = get_user_input(
                "AWS Secret Access Key",
                "Corresponding secret key for the Access Key ID above",
                current_value=env_vars.get('AWS_SECRET_ACCESS_KEY', '')
            )
    
    # Save the configuration
    print(f"\n{Colors.BOLD}💾 SAVING CONFIGURATION{Colors.END}")
    print("-" * 50)
    
    if save_env_file(env_vars):
        print(f"\n{Colors.GREEN}🎉 Setup complete!{Colors.END}")
        print(f"{Colors.GREEN}Your .env file has been created/updated.{Colors.END}\n")
        
        # Test the APIs
        test_now = input(f"Test your API keys now? (Y/n): ").lower().strip()
        if test_now != 'n':
            print(f"\n{Colors.BLUE}🧪 Running API tests...{Colors.END}\n")
            try:
                os.system(f"{sys.executable} test_api_keys.py")
            except Exception as e:
                print(f"{Colors.RED}Error running tests: {e}{Colors.END}")
                print(f"{Colors.YELLOW}You can run tests manually with: python test_api_keys.py{Colors.END}")
        
        print(f"\n{Colors.CYAN}📚 Next Steps:{Colors.END}")
        print(f"1. Review the API_KEYS_GUIDE.md for detailed instructions")
        print(f"2. Run: python test_api_keys.py (to test your keys)")
        print(f"3. Run: python tactical_server.py (to start the simulation)")
        print(f"4. Open: http://localhost:8000/tactical-map (to view the 3D interface)")
        
    else:
        print(f"\n{Colors.RED}❌ Setup failed. Please check file permissions and try again.{Colors.END}")

if __name__ == "__main__":
    main()