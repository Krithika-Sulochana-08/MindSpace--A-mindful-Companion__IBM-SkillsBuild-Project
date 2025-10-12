import os
import requests
import streamlit as st

class OpenRouterClient:
    def __init__(self, api_key: str | None = None):
        """Initialize with API key from Streamlit secrets or environment"""
        self.api_key = (
            api_key
            or st.secrets.get("OPENROUTER_API_KEY")
            or os.getenv("OPENROUTER_API_KEY")
        )
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        # Use a public, fully accessible model for testing
        self.model = "mistralai/mistral-7b-instruct"

    def generate_response(self, user_input: str) -> str:
        if not self.api_key:
            return "Missing OpenRouter API key. Please add it in Streamlit secrets."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # ⚠️ MUST exactly match your Streamlit app domain:
            "HTTP-Referer": "https://mindspace--a-mindful-companionibm-skillsbuild-project-xrcpappc.streamlit.app/",
            "X-Title": "MindSpace - A Mindful Companion"
        }

        system_message = (
            "You are a compassionate, empathetic mental health companion. "
            "Provide warm, supportive, and emotionally safe responses. "
            "Never offer diagnoses or replace therapy. "
            "Encourage professional help when necessary."
        )

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input},
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            elif response.status_code == 401:
                return "I'm here to listen. The OpenRouter API key or headers were rejected. Please verify your credentials."
            elif response.status_code == 429:
                return "I'm here to listen. The service is currently rate-limited. Please try again shortly."
            else:
                return f"I'm here to listen. Unexpected error: {response.status_code} - {response.text[:200]}"

        except requests.exceptions.Timeout:
            return "The response is taking a bit longer than expected. Let's take a deep breath together."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

# Create a global instance
openrouter_client = OpenRouterClient()
