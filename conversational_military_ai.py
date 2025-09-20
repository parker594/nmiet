#!/usr/bin/env python3
"""
🎖️ CONVERSATIONAL MILITARY AI ASSISTANT
Real conversational AI with context understanding and human-like responses
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

class ConversationalMilitaryAI:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.conversation_history = []
        self.user_context = {
            "name": "Commander",
            "rank": "Unknown",
            "preferences": {},
            "current_mission": None
        }
        
        # Current military situation (dynamic data)
        self.current_situation = {
            "location": "Pune Military Command Center",
            "time": datetime.now().strftime("%H:%M"),
            "threat_level": "MODERATE",
            "active_alerts": [],
            "recent_events": []
        }
        
        # AI Personality and behavior
        self.ai_personality = {
            "style": "professional_military",
            "tone": "helpful_and_direct",
            "expertise": "tactical_analysis",
            "memory": True,
            "context_awareness": True
        }
    
    def print_startup(self):
        """Display startup message"""
        print("\n" + "="*70)
        print("🎖️  CONVERSATIONAL MILITARY AI ASSISTANT")
        print("="*70)
        print("🤖 AI: Good day, Commander. I'm your personal military AI assistant.")
        print("🤖 AI: I can understand context, remember our conversation, and provide")
        print("🤖 AI: human-like responses tailored to your specific needs.")
        print("\nType your message naturally - I'll understand and respond appropriately.")
        print("Commands: 'setup' (configure pipelines), 'exit' (quit)")
        print("="*70 + "\n")
    
    def setup_pipelines(self):
        """Interactive pipeline setup"""
        print("\n🔧 PIPELINE CONFIGURATION SYSTEM")
        print("="*50)
        print("I can set up different response pipelines for different types of tasks:")
        print("\n1. 📊 INTELLIGENCE ANALYSIS PIPELINE")
        print("   - Threat assessment and analysis")
        print("   - Sensor data interpretation")
        print("   - Strategic intelligence reports")
        
        print("\n2. ⚔️  TACTICAL OPERATIONS PIPELINE") 
        print("   - Mission planning and execution")
        print("   - Unit deployment strategies")
        print("   - Combat operations guidance")
        
        print("\n3. 🚨 EMERGENCY RESPONSE PIPELINE")
        print("   - Crisis management protocols")
        print("   - Evacuation procedures")
        print("   - Emergency decision support")
        
        print("\n4. 📋 LOGISTICS & PLANNING PIPELINE")
        print("   - Resource management")
        print("   - Supply chain optimization")
        print("   - Personnel coordination")
        
        print("\n5. 🤖 CONVERSATIONAL GENERAL PIPELINE")
        print("   - Natural conversation and questions")
        print("   - Context-aware responses")
        print("   - Learning from interactions")
        
        pipeline_choice = input("\nWhich pipeline would you like to configure? (1-5 or 'all'): ").strip()
        
        if pipeline_choice == 'all':
            self.configure_all_pipelines()
        elif pipeline_choice in ['1', '2', '3', '4', '5']:
            self.configure_specific_pipeline(int(pipeline_choice))
        else:
            print("🤖 AI: I'll keep the default conversational setup for now.")
    
    def configure_all_pipelines(self):
        """Configure all pipelines"""
        print("\n🤖 AI: Excellent! I'm configuring all response pipelines for you.")
        print("This will give me specialized capabilities for different types of requests:")
        
        self.ai_personality["pipelines"] = {
            "intelligence": {
                "style": "analytical_detailed",
                "format": "structured_report",
                "focus": "data_analysis"
            },
            "tactical": {
                "style": "decisive_action_oriented", 
                "format": "operational_brief",
                "focus": "mission_success"
            },
            "emergency": {
                "style": "calm_urgent",
                "format": "priority_action_list",
                "focus": "immediate_response"
            },
            "logistics": {
                "style": "systematic_efficient",
                "format": "resource_optimization",
                "focus": "coordination"
            },
            "conversational": {
                "style": "natural_adaptive",
                "format": "dialogue",
                "focus": "understanding"
            }
        }
        
        print("✅ All pipelines configured! I can now adapt my responses based on context.")
        print("🤖 AI: Try asking me different types of questions and see how I adapt!")
    
    def configure_specific_pipeline(self, pipeline_num):
        """Configure a specific pipeline"""
        pipeline_names = {
            1: "Intelligence Analysis",
            2: "Tactical Operations", 
            3: "Emergency Response",
            4: "Logistics & Planning",
            5: "Conversational General"
        }
        
        print(f"\n🤖 AI: Configuring {pipeline_names[pipeline_num]} pipeline...")
        print("✅ Pipeline ready! I'll use specialized responses for this type of request.")
    
    def detect_intent_and_pipeline(self, user_input):
        """Detect user intent and select appropriate pipeline"""
        user_lower = user_input.lower()
        
        # Intelligence/Analysis keywords
        if any(word in user_lower for word in ['analyze', 'assess', 'intelligence', 'threat', 'data', 'sensor', 'report']):
            return "intelligence"
        
        # Tactical/Operations keywords  
        elif any(word in user_lower for word in ['deploy', 'tactical', 'mission', 'strategy', 'operation', 'attack', 'defense']):
            return "tactical"
        
        # Emergency keywords
        elif any(word in user_lower for word in ['emergency', 'urgent', 'evacuation', 'crisis', 'alert', 'immediate']):
            return "emergency"
        
        # Logistics keywords
        elif any(word in user_lower for word in ['supply', 'logistics', 'resources', 'personnel', 'equipment', 'coordinate']):
            return "logistics"
        
        # Default to conversational
        else:
            return "conversational"
    
    def get_conversational_response(self, user_input, pipeline="conversational"):
        """Get truly conversational response from AI"""
        if not self.openai_api_key:
            return "🤖 AI: I need my OpenAI connection to give you proper conversational responses. Currently running in basic mode."
        
        try:
            # Build conversation context
            context_messages = [
                {
                    "role": "system",
                    "content": f"""You are a highly intelligent military AI assistant with a natural, conversational personality. 

PERSONALITY TRAITS:
- Speak naturally like a knowledgeable military advisor who cares about the user
- Remember and reference previous parts of our conversation
- Ask follow-up questions when appropriate
- Adapt your communication style to what the user needs
- Be helpful, direct, but also personable
- Use military knowledge but explain things clearly

CURRENT CONTEXT:
- Location: {self.current_situation['location']}
- Time: {self.current_situation['time']}
- Pipeline: {pipeline}
- User: {self.user_context['name']}

RESPONSE STYLE FOR {pipeline.upper()} PIPELINE:
{self.get_pipeline_instructions(pipeline)}

Remember our conversation history and respond naturally. Don't just give reports - have a real conversation."""
                }
            ]
            
            # Add conversation history (last 5 exchanges)
            for exchange in self.conversation_history[-5:]:
                context_messages.append({"role": "user", "content": exchange["user"]})
                context_messages.append({"role": "assistant", "content": exchange["ai"]})
            
            # Add current user input
            context_messages.append({"role": "user", "content": user_input})
            
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": context_messages,
                "max_tokens": 600,
                "temperature": 0.8,  # Higher for more natural conversation
                "presence_penalty": 0.1,
                "frequency_penalty": 0.1
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
                
                # Store in conversation history
                self.conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": user_input,
                    "ai": ai_response,
                    "pipeline": pipeline
                })
                
                return ai_response
            else:
                return f"🤖 AI: I'm having trouble connecting to my advanced systems (Error {response.status_code}). Let me give you a basic response instead."
                
        except Exception as e:
            return f"🤖 AI: I encountered an issue ({e}). Let me try to help you anyway - what specifically do you need assistance with?"
    
    def get_pipeline_instructions(self, pipeline):
        """Get specific instructions for each pipeline"""
        instructions = {
            "intelligence": "Provide analytical, data-driven responses with specific details and actionable intelligence. Be thorough but clear.",
            "tactical": "Give decisive, action-oriented advice focused on mission success. Be direct and strategic.",
            "emergency": "Respond with calm urgency, prioritizing immediate actions and safety. Be clear and decisive.",
            "logistics": "Focus on coordination, resource optimization, and systematic planning. Be organized and efficient.",
            "conversational": "Have a natural conversation, ask follow-up questions, and adapt to the user's communication style."
        }
        return instructions.get(pipeline, instructions["conversational"])
    
    def handle_special_commands(self, user_input):
        """Handle special commands"""
        command = user_input.lower().strip()
        
        if command == 'setup':
            self.setup_pipelines()
            return True
        elif command in ['exit', 'quit', 'goodbye']:
            print("\n🤖 AI: It's been great working with you, Commander. Stay safe out there!")
            print("Until next time - mission success! 🎖️\n")
            return False
        elif command == 'history':
            print(f"\n📚 CONVERSATION HISTORY ({len(self.conversation_history)} exchanges):")
            for i, exchange in enumerate(self.conversation_history[-5:], 1):
                print(f"\n{i}. YOU: {exchange['user']}")
                print(f"   AI: {exchange['ai'][:100]}...")
            print()
            return True
        elif command == 'clear':
            self.conversation_history = []
            print("🤖 AI: Conversation history cleared. Fresh start!")
            return True
            
        return None
    
    def run(self):
        """Main conversation loop"""
        self.print_startup()
        
        while True:
            try:
                # Get user input
                user_input = input("👤 YOU: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                command_result = self.handle_special_commands(user_input)
                if command_result == False:  # Exit
                    break
                elif command_result == True:  # Command processed
                    continue
                
                # Detect intent and pipeline
                pipeline = self.detect_intent_and_pipeline(user_input)
                
                # Show pipeline detection (optional)
                if hasattr(self.ai_personality, 'pipelines'):
                    print(f"🔄 [Using {pipeline.title()} Pipeline]")
                
                # Get AI response
                print("🤖 AI: ", end="", flush=True)
                
                # Simulate thinking time
                time.sleep(0.5)
                
                response = self.get_conversational_response(user_input, pipeline)
                print(response)
                print()  # Extra line for readability
                
            except KeyboardInterrupt:
                print("\n\n🤖 AI: Understood. Ending our session. Take care, Commander! 🎖️\n")
                break
            except Exception as e:
                print(f"\n🤖 AI: I encountered an error: {e}")
                print("Let's continue our conversation anyway.\n")
                continue

if __name__ == "__main__":
    try:
        ai_assistant = ConversationalMilitaryAI()
        ai_assistant.run()
    except Exception as e:
        print(f"❌ System Error: {e}")
        sys.exit(1)