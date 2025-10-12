import requests
import streamlit as st
import os

class OpenRouterClient:
    def __init__(self):
        self.setup_api_key()
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "meta-llama/llama-3.1-8b-instruct"
        
    def setup_api_key(self):
        """Setup OpenRouter API key"""
        try:
            self.api_key = st.secrets["OPENROUTER_API_KEY"]
        except:
            self.api_key = os.getenv("OPENROUTER_API_KEY")
            if not self.api_key:
                st.error("Please set OPENROUTER_API_KEY in your environment variables or Streamlit secrets")
                st.stop()
    
    def generate_response(self, user_input):
        """Generate response using OpenRouter API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://localhost:8501",
                "X-Title": "Mental Health Companion"
            }
            
            system_message = """You are a compassionate, empathetic mental health companion. Your role is to provide supportive listening, help users explore their feelings, and offer gentle guidance. Always prioritize emotional safety and validation.

Guidelines:
- Be warm, non-judgmental, and validating
- Ask open-ended questions to help users explore their feelings
- Never provide medical diagnoses or replace professional therapy
- Encourage professional help when needed
- Focus on coping strategies and emotional awareness
- Maintain appropriate boundaries
- Keep responses conversational and natural (2-4 sentences typically)

Important: You are NOT a licensed therapist. Always encourage professional help for serious concerns."""

            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                error_msg = f"Status: {response.status_code}"
                return f"I'm here to listen. How are you feeling today? ({error_msg})"
                
        except requests.exceptions.Timeout:
            return "I'm here to listen. The response is taking longer than usual. What's on your mind?"
        except Exception as e:
            return f"I'm here to listen. How are you feeling today? (Error: {str(e)})"

# Create global instance
openrouter_client = OpenRouterClient()