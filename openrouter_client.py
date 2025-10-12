import os
import requests
import streamlit as st

class OpenRouterClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = (
            api_key
            or st.secrets.get("OPENROUTER_API_KEY")
            or os.getenv("OPENROUTER_API_KEY")
        )
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        # Use a public model for testing
        self.model = "mistralai/mistral-7b-instruct"

    def generate_response(self, user_input: str) -> str:
        if not self.api_key:
            return "I'm here to listen. Missing OpenRouter API key."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # ⚠️ IMPORTANT: must match your Streamlit Cloud app URL
            "HTTP-Referer": "https://mindspace--a-mindful-companionibm-skillsbuild-project-xrcpappc.streamlit.app/",
            "X-Title": "MindSpace - A Mindful Companion",
        }

        system_message = (
            "You are a compassionate, empathetic mental health companion. "
            "Provide warm, supportive, and emotionally safe responses. "
            "Never offer diagnoses or replace therapy."
        )

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input},
            ],
            "max_tokens": 300,
            "temperature": 0.7,
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            elif response.status_code == 401:
                return "The AI service rejected our credentials. Please verify the API key or headers."
            else:
                return f"Error {response.status_code}: {response.text[:200]}"

        except Exception as e:
            return f"Network error: {str(e)}"

# global instance
openrouter_client = OpenRouterClient()
