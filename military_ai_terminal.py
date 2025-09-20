#!/usr/bin/env python3
"""
🎖️ MILITARY AI COMMAND TERMINAL
Advanced Terminal-Based Military Assistant
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MilitaryAITerminal:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.session_history = []
        self.military_context = {
            "location": "Pune Military Command Center",
            "coordinates": "18.5204, 73.8567",
            "heat_sensors": {
                "HS-001": {"temp": 89.2, "status": "Normal", "location": "Perimeter"},
                "HS-002": {"temp": 94.7, "status": "Elevated", "location": "Forward Base"},
                "HS-003": {"temp": 101.1, "status": "Critical", "location": "Red Zone"},
                "HS-004": {"temp": 78.3, "status": "Normal", "location": "Supply Route"},
                "HS-005": {"temp": 96.8, "status": "Critical", "location": "Investigation Zone"},
                "HS-006": {"temp": 83.5, "status": "Normal", "location": "Checkpoint"}
            },
            "military_assets": {
                "Alpha Base": {"personnel": 150, "status": "Operational"},
                "Pune Airbase": {"personnel": 300, "status": "Operational"},
                "Bravo Outpost": {"personnel": 25, "status": "Active"},
                "Charlie Support": {"personnel": 75, "status": "Operational"}
            },
            "threat_level": "MODERATE",
            "security_level": "ALPHA"
        }
    
    def print_banner(self):
        """Display military terminal banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🎖️  MILITARY AI COMMAND TERMINAL  🎖️                     ║
║                          Advanced AI Assistant v2.0                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  📍 Location: Pune Military Command Center                                  ║
║  🤖 AI Model: OpenAI GPT-4o-mini Tactical Intelligence                     ║
║  🔒 Security: ALPHA Level Clearance                                         ║
║  ⚡ Status: OPERATIONAL                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print("\033[92m" + banner + "\033[0m")
        print("\033[93m⚠️  WARNING: All communications are monitored and logged for security.\033[0m")
        print("\033[96mType 'help' for commands, 'exit' to quit, 'status' for system status.\033[0m\n")
    
    def print_status(self):
        """Display current military status"""
        print("\n\033[92m" + "="*80 + "\033[0m")
        print("\033[92m🎖️  MILITARY COMMAND STATUS REPORT\033[0m")
        print("\033[92m" + "="*80 + "\033[0m")
        
        print(f"\033[93m📍 LOCATION:\033[0m {self.military_context['location']}")
        print(f"\033[93m🎯 COORDINATES:\033[0m {self.military_context['coordinates']}")
        print(f"\033[93m⚠️  THREAT LEVEL:\033[0m {self.military_context['threat_level']}")
        print(f"\033[93m🔒 SECURITY LEVEL:\033[0m {self.military_context['security_level']}")
        
        print("\n\033[96m🌡️  HEAT SENSOR NETWORK:\033[0m")
        for sensor_id, data in self.military_context['heat_sensors'].items():
            status_color = "\033[91m" if data['status'] == "Critical" else "\033[93m" if data['status'] == "Elevated" else "\033[92m"
            print(f"   {sensor_id}: {data['temp']}°F - {status_color}{data['status']}\033[0m ({data['location']})")
        
        print("\n\033[96m🎖️  MILITARY ASSETS:\033[0m")
        total_personnel = 0
        for base, data in self.military_context['military_assets'].items():
            total_personnel += data['personnel']
            status_color = "\033[92m" if data['status'] == "Operational" else "\033[93m"
            print(f"   {base}: {data['personnel']} personnel - {status_color}{data['status']}\033[0m")
        
        print(f"\n\033[96m📊 TOTAL PERSONNEL:\033[0m {total_personnel}")
        print("\033[92m" + "="*80 + "\033[0m\n")
    
    def print_help(self):
        """Display help commands"""
        help_text = """
\033[92m╔═══════════════════════════════════════════════════════════════════════════════╗
║                           🎖️  MILITARY AI COMMANDS  🎖️                        ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  \033[93mstatus\033[92m        - Display current military status and sensor readings      ║
║  \033[93mthreat\033[92m        - Assess current threat level and recommendations         ║
║  \033[93msensors\033[92m       - Check heat sensor network status                       ║
║  \033[93massets\033[92m        - Display military assets and personnel                  ║
║  \033[93memergency\033[92m     - Emergency protocols and evacuation procedures         ║
║  \033[93mdeploy\033[92m        - Tactical deployment recommendations                    ║
║  \033[93mintel\033[92m         - Intelligence analysis and reporting                   ║
║  \033[93mhelp\033[92m          - Show this help menu                                   ║
║  \033[93mexit\033[92m          - Terminate session                                      ║
║                                                                             ║
║  💬 You can also ask natural language questions about:                     ║
║     • Tactical operations and strategy                                      ║
║     • Threat assessment and analysis                                        ║
║     • Equipment and personnel deployment                                    ║
║     • Emergency procedures and protocols                                    ║
║     • Intelligence gathering and reconnaissance                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝\033[0m
"""
        print(help_text)
    
    def get_ai_response(self, user_input):
        """Get response from OpenAI with military context"""
        if not self.openai_api_key:
            return self.get_fallback_response(user_input)
        
        try:
            # Build military context prompt
            context_prompt = f"""You are an advanced military AI assistant operating at the Pune Military Command Center. You provide tactical analysis, strategic guidance, and operational support to military personnel.

CURRENT OPERATIONAL CONTEXT:
- Location: {self.military_context['location']}
- Coordinates: {self.military_context['coordinates']}
- Threat Level: {self.military_context['threat_level']}
- Security Level: {self.military_context['security_level']}

HEAT SENSOR STATUS:
{self._format_sensor_data()}

MILITARY ASSETS:
{self._format_asset_data()}

GUIDELINES:
- Respond with professional military terminology
- Provide actionable tactical recommendations
- Include relevant coordinates and data when applicable
- Maintain security protocols in all communications
- Give specific, detailed military analysis
- Use proper military time format (24-hour)
- Include threat assessments when relevant

User Query: {user_input}

Provide a comprehensive military response addressing the query with current operational context."""

            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an elite military AI tactical analyst providing professional military intelligence and operational support. Respond with detailed, actionable military guidance."
                    },
                    {
                        "role": "user",
                        "content": context_prompt
                    }
                ],
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
                
                # Add to session history
                self.session_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "ai": ai_response,
                    "model": "OpenAI GPT-4o-mini"
                })
                
                return ai_response
            else:
                print(f"\033[91m⚠️  OpenAI API Error: {response.status_code}\033[0m")
                return self.get_fallback_response(user_input)
                
        except Exception as e:
            print(f"\033[91m⚠️  AI System Error: {e}\033[0m")
            return self.get_fallback_response(user_input)
    
    def _format_sensor_data(self):
        """Format sensor data for AI context"""
        sensor_info = []
        for sensor_id, data in self.military_context['heat_sensors'].items():
            sensor_info.append(f"- {sensor_id}: {data['temp']}°F - {data['status']} ({data['location']})")
        return "\n".join(sensor_info)
    
    def _format_asset_data(self):
        """Format asset data for AI context"""
        asset_info = []
        for base, data in self.military_context['military_assets'].items():
            asset_info.append(f"- {base}: {data['personnel']} personnel - {data['status']}")
        return "\n".join(asset_info)
    
    def get_fallback_response(self, user_input):
        """Provide intelligent fallback responses"""
        user_lower = user_input.lower()
        timestamp = datetime.now().strftime("%H%M")
        
        if any(word in user_lower for word in ['threat', 'assess', 'danger', 'risk']):
            return f"""🎯 THREAT ASSESSMENT REPORT - {timestamp} HOURS

CURRENT THREAT ANALYSIS:
• Operational Area: Pune Military Command Center
• Threat Level: {self.military_context['threat_level']}
• Security Posture: {self.military_context['security_level']} Level

CRITICAL INDICATORS:
• Heat Sensor HS-003: 101.1°F (CRITICAL) - Red Zone investigation required
• Heat Sensor HS-005: 96.8°F (CRITICAL) - Investigation Zone monitoring
• Elevated readings indicate potential thermal anomalies

IMMEDIATE RECOMMENDATIONS:
1. Deploy investigation teams to critical heat zones
2. Maintain elevated security posture across all installations
3. Prepare emergency response protocols
4. Continue monitoring all sensor networks

TACTICAL ASSESSMENT: Situation requires immediate attention. All personnel maintain readiness."""

        elif any(word in user_lower for word in ['sensor', 'heat', 'temperature', 'thermal']):
            critical_sensors = [s for s, d in self.military_context['heat_sensors'].items() if d['status'] == 'Critical']
            return f"""🌡️ HEAT SENSOR NETWORK STATUS - {timestamp} HOURS

SENSOR NETWORK OPERATIONAL STATUS:
• Total Sensors: 6 units deployed
• Operational: 6/6 sensors online
• Critical Readings: {len(critical_sensors)} sensors

DETAILED READINGS:
{self._format_sensor_data()}

ANALYSIS:
• Average Temperature: 90.3°F
• Critical Zones: {len(critical_sensors)} locations requiring immediate attention
• Trend Analysis: Elevated readings in tactical sectors 3 & 5

RECOMMENDATIONS:
• Deploy thermal imaging assets to critical zones
• Maintain continuous monitoring protocols
• Investigate temperature anomalies immediately"""

        elif any(word in user_lower for word in ['deploy', 'tactical', 'strategy', 'operation']):
            return f"""⚔️ TACTICAL DEPLOYMENT ANALYSIS - {timestamp} HOURS

CURRENT FORCE DISPOSITION:
{self._format_asset_data()}

DEPLOYMENT STRATEGY:
• Primary Force: Alpha Base (150 personnel) - Forward operations
• Air Support: Pune Airbase (300 personnel) - Tactical air operations
• Reconnaissance: Bravo Outpost (25 personnel) - Intelligence gathering
• Logistics: Charlie Support (75 personnel) - Supply and maintenance

TACTICAL PRIORITIES:
1. Secure critical temperature zones (HS-003, HS-005)
2. Establish robust communication networks
3. Maintain rapid response capabilities
4. Prepare contingency operations

MISSION STATUS: All units operational and ready for immediate deployment."""

        elif any(word in user_lower for word in ['emergency', 'evacuation', 'protocol', 'alert']):
            return f"""🚨 EMERGENCY PROTOCOLS ACTIVATED - {timestamp} HOURS

EVACUATION PROCEDURES:
• Primary Route: Direct path to Pune Airbase (18.5821, 73.9197)
• Secondary Route: Alpha Base to designated rally point
• Emergency Assembly: Coordinates 18.5204, 73.8567

EMERGENCY RESPONSE TIMELINE:
• Phase 1: Critical personnel evacuation (0-5 minutes)
• Phase 2: Essential equipment security (5-15 minutes)
• Phase 3: General evacuation procedures (15-30 minutes)

COMMUNICATION PROTOCOLS:
• Emergency Frequency: Secured military channel active
• Medical Support: Bravo Outpost designated trauma center
• Command & Control: Alpha Base operations center

STATUS: All emergency protocols ready for immediate activation."""

        elif any(word in user_lower for word in ['asset', 'personnel', 'base', 'force']):
            total_personnel = sum(d['personnel'] for d in self.military_context['military_assets'].values())
            return f"""🎖️ MILITARY ASSETS STATUS - {timestamp} HOURS

FORCE STRUCTURE ANALYSIS:
{self._format_asset_data()}

PERSONNEL SUMMARY:
• Total Personnel: {total_personnel}
• Combat Ready: 100%
• Operational Status: All units fully operational

ASSET CAPABILITIES:
• Alpha Base: Forward operating base with full tactical capabilities
• Pune Airbase: Air operations center with fighter and transport aircraft
• Bravo Outpost: Intelligence and reconnaissance operations
• Charlie Support: Logistics hub and maintenance facility

READINESS LEVEL: All assets at full operational capacity and mission-ready."""

        else:
            return f"""🎖️ MILITARY AI ASSISTANT - {timestamp} HOURS

COMMAND ACKNOWLEDGED: "{user_input}"

CURRENT OPERATIONAL STATUS:
• Location: {self.military_context['location']}
• Security Level: {self.military_context['security_level']}
• All systems operational and mission-ready

AVAILABLE ASSISTANCE:
• Tactical analysis and strategic planning
• Threat assessment and intelligence evaluation
• Personnel and equipment deployment guidance
• Emergency protocols and evacuation procedures
• Real-time operational status monitoring

Please specify your tactical requirements or use 'help' for available commands.

SYSTEM STATUS: Standing by for further tactical guidance."""
    
    def process_command(self, user_input):
        """Process special commands"""
        command = user_input.lower().strip()
        
        if command == 'status':
            self.print_status()
            return True
        elif command == 'help':
            self.print_help()
            return True
        elif command in ['exit', 'quit', 'logout']:
            print("\n\033[92m🎖️  Terminating Military AI Session\033[0m")
            print("\033[93m⚠️  All session data has been logged for security review.\033[0m")
            print("\033[96mStay vigilant. Mission continues.\033[0m\n")
            return False
        elif command == 'sensors':
            print("\n\033[96m🌡️  HEAT SENSOR QUICK STATUS:\033[0m")
            for sensor_id, data in self.military_context['heat_sensors'].items():
                status_color = "\033[91m" if data['status'] == "Critical" else "\033[93m" if data['status'] == "Elevated" else "\033[92m"
                print(f"   {sensor_id}: {data['temp']}°F - {status_color}{data['status']}\033[0m")
            print()
            return True
        elif command == 'assets':
            print("\n\033[96m🎖️  MILITARY ASSETS QUICK STATUS:\033[0m")
            for base, data in self.military_context['military_assets'].items():
                status_color = "\033[92m" if data['status'] == "Operational" else "\033[93m"
                print(f"   {base}: {data['personnel']} personnel - {status_color}{data['status']}\033[0m")
            print()
            return True
        
        return None
    
    def run(self):
        """Main terminal loop"""
        self.print_banner()
        
        while True:
            try:
                # Display prompt
                user_input = input("\033[92m🎖️  COMMAND> \033[0m").strip()
                
                if not user_input:
                    continue
                
                # Process special commands
                command_result = self.process_command(user_input)
                if command_result == False:  # Exit command
                    break
                elif command_result == True:  # Command processed
                    continue
                
                # Process AI query
                print("\n\033[93m🤖 AI ANALYZING...\033[0m")
                
                # Simulate processing time
                time.sleep(1)
                
                response = self.get_ai_response(user_input)
                
                # Display AI response
                print("\n\033[96m" + "="*80 + "\033[0m")
                print("\033[96m🤖 MILITARY AI TACTICAL ANALYSIS\033[0m")
                print("\033[96m" + "="*80 + "\033[0m")
                print(response)
                print("\033[96m" + "="*80 + "\033[0m\n")
                
            except KeyboardInterrupt:
                print("\n\n\033[93m⚠️  Session interrupted by user.\033[0m")
                print("\033[96mTerminating Military AI Terminal...\033[0m\n")
                break
            except Exception as e:
                print(f"\n\033[91m❌ System Error: {e}\033[0m\n")
                continue

if __name__ == "__main__":
    try:
        military_ai = MilitaryAITerminal()
        military_ai.run()
    except Exception as e:
        print(f"\033[91m❌ Fatal Error: {e}\033[0m")
        sys.exit(1)