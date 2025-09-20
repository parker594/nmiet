#!/usr/bin/env python3
"""
🎖️ INTELLIGENT MILITARY AI AGENT
Natural conversation with military focus - no keywords needed
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

class IntelligentMilitaryAgent:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.conversation_memory = []
        
        # Military context that the AI always knows about
        self.military_knowledge_base = {
            "current_base": "Pune Military Command Center",
            "coordinates": "18.5204°N, 73.8567°E",
            "active_operations": "Heat monitoring, Perimeter security, Intelligence gathering",
            "current_status": "Operational readiness level ALPHA",
            "available_assets": "4 military bases, 6 heat sensors, 550+ personnel"
        }
    
    def print_welcome(self):
        """Simple welcome message"""
        print("\n" + "="*60)
        print("🎖️  MILITARY AI AGENT - INTELLIGENT CONVERSATION")
        print("="*60)
        print("🤖 AI: Hello! I'm your military AI assistant.")
        print("🤖 AI: Just talk to me naturally - I understand everything!")
        print("🤖 AI: I'll keep our conversation military-focused when needed.")
        print("\nType 'exit' to quit, or just start chatting!")
        print("="*60 + "\n")
    
    def get_intelligent_response(self, user_message):
        """Get natural, intelligent response from OpenAI"""
        if not self.openai_api_key:
            return "🤖 AI: I need my OpenAI connection to have a proper conversation with you. Please check the API key configuration."
        
        try:
            # Build the conversation with military personality and context
            system_prompt = f"""You are an intelligent military AI assistant. Here's what you need to know:

PERSONALITY:
- You're helpful, professional, but also conversational and natural
- You understand context and can talk about anything
- When topics go off-military, you gently guide back to military/tactical matters
- You remember our conversation and build on it
- You're knowledgeable about military operations, tactics, and procedures

CURRENT MILITARY CONTEXT:
- Base: {self.military_knowledge_base['current_base']}
- Location: {self.military_knowledge_base['coordinates']}
- Operations: {self.military_knowledge_base['active_operations']}
- Status: {self.military_knowledge_base['current_status']}
- Assets: {self.military_knowledge_base['available_assets']}

BEHAVIOR GUIDELINES:
1. Respond naturally to whatever the human says
2. If they ask about non-military topics, acknowledge it but relate it back to military context
3. Remember what they've told you in our conversation
4. Be conversational - ask follow-up questions, show interest
5. Use your military knowledge when relevant
6. Don't force military topics, but keep the overall focus professional

Example of handling off-topic:
Human: "What's the weather like?"
You: "I don't have current weather data, but weather conditions are crucial for military operations. Are you asking because you're planning an outdoor operation or mission? I can help you think through weather considerations for tactical planning."

Be natural, intelligent, and helpful while maintaining military professionalism."""

            # Prepare conversation history
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add recent conversation history (last 8 messages to keep context)
            for exchange in self.conversation_memory[-4:]:
                messages.append({"role": "user", "content": exchange["user"]})
                messages.append({"role": "assistant", "content": exchange["ai"]})
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Make API call
            headers = {
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-4o-mini",
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.8,  # Natural conversation
                "presence_penalty": 0.2,  # Encourage variety
                "frequency_penalty": 0.1   # Reduce repetition
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
                
                # Save to conversation memory
                self.conversation_memory.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "user": user_message,
                    "ai": ai_response
                })
                
                # Keep only last 10 exchanges to manage memory
                if len(self.conversation_memory) > 10:
                    self.conversation_memory = self.conversation_memory[-10:]
                
                return ai_response
            
            elif response.status_code == 429:
                return "🤖 AI: I'm getting a lot of requests right now. Can you try again in a moment?"
            
            else:
                return f"🤖 AI: I'm having some technical difficulties (Error {response.status_code}). But I'm still here to help you - what do you need?"
                
        except requests.exceptions.Timeout:
            return "🤖 AI: My response took too long - the network might be slow. What were you asking about?"
        
        except Exception as e:
            return f"🤖 AI: I encountered an issue: {str(e)[:50]}... But I'm still here! What can I help you with?"
    
    def handle_commands(self, user_input):
        """Handle simple commands"""
        command = user_input.lower().strip()
        
        if command in ['exit', 'quit', 'bye', 'goodbye']:
            print("\n🤖 AI: Take care! It's been great talking with you. 🎖️")
            print("Stay safe out there, and feel free to come back anytime!\n")
            return False
        
        elif command in ['clear', 'reset']:
            self.conversation_memory = []
            print("🤖 AI: Memory cleared! Let's start fresh. What's on your mind?")
            return True
        
        elif command in ['help', '?']:
            print("\n🤖 AI: I'm here to help with anything you need!")
            print("Just talk to me naturally - I understand context and remember our conversation.")
            print("Commands: 'clear' (reset memory), 'exit' (quit)")
            print("But honestly, just chat with me like you would with any assistant!\n")
            return True
        
        return None
    
    def run(self):
        """Main conversation loop"""
        self.print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = input("👤 YOU: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                command_result = self.handle_commands(user_input)
                if command_result == False:  # Exit
                    break
                elif command_result == True:  # Command processed
                    continue
                
                # Get AI response
                print("🤖 AI: ", end="", flush=True)
                
                # Small delay for natural feel
                time.sleep(0.3)
                
                response = self.get_intelligent_response(user_input)
                print(response)
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n\n🤖 AI: Understood. Take care! 🎖️\n")
                break
            except Exception as e:
                print(f"\n🤖 AI: Something went wrong: {e}")
                print("But I'm still here to help! What do you need?\n")
                continue

if __name__ == "__main__":
    try:
        print("🔄 Starting Intelligent Military AI Agent...")
        agent = IntelligentMilitaryAgent()
        agent.run()
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        sys.exit(1)