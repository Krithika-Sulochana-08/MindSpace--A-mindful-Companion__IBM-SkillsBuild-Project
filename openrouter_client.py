import os
import requests
import streamlit as st

class OpenRouterClient:
    def __init__(self, api_key: str | None = None):
        """
        Initialize client. Prefer explicit api_key, then Streamlit secrets, then environment variable.
        This constructor will NOT call st.stop() to avoid crashing during import on Streamlit Cloud;
        instead, it sets self.api_key to None and generate_response will return a friendly message.
        """
        # Prefer explicit, then Streamlit secret, then env var
        self.api_key = (
            api_key
            or st.secrets.get("OPENROUTER_API_KEY")  # Streamlit Cloud
            or os.getenv("OPENROUTER_API_KEY")      # Local env
        )
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        # Default model (you can change)
        self.model = "meta-llama/llama-3.1-8b-instruct"

    def _missing_key_message(self):
        return (
            "I'm here to listen. It looks like the service key is not configured. "
            "Please ask the app owner to set OPENROUTER_API_KEY in Streamlit secrets or environment variables."
        )

    def generate_response(self, user_input: str) -> str:
        """Generate response using OpenRouter API. Returns a user-friendly string on any failure."""
        # Check for API key
        if not self.api_key:
            # Don't call st.stop() here; return a friendly message to the UI
            return self._missing_key_message()

        # Build headers
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # Prefer real deployed app referer if known; fallback to localhost (not required)
            "HTTP-Referer": os.getenv("STREAMLIT_DEPLOY_URL", "https://your-app.streamlit.app"),
            "X-Title": "Mental Health Companion",
        }

        # System prompt - compassionate assistant
        system_message = (
            "You are a compassionate, empathetic mental health companion. Your role is to provide "
            "supportive listening, help users explore their feelings, and offer gentle guidance. "
            "Always prioritize emotional safety and validation.\n\n"
            "Guidelines:\n"
            "- Be warm, non-judgmental, and validating\n"
            "- Ask open-ended questions to help users explore their feelings\n"
            "- Never provide medical diagnoses or replace professional therapy\n"
            "- Encourage professional help when needed\n"
            "- Focus on coping strategies and emotional awareness\n"
            "- Maintain appropriate boundaries\n"
            "- Keep responses conversational and natural (2-4 sentences typically)\n\n"
            "Important: You are NOT a licensed therapist. Always encourage professional help for serious concerns."
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input},
            ],
            # optional tuning parameters
            "max_tokens": 500,
            "temperature": 0.7,
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
        except requests.exceptions.Timeout:
            return "I'm here to listen. The response is taking longer than usual. What's on your mind?"
        except requests.exceptions.RequestException as e:
            # Generic network error
            return f"I'm here to listen. There was a network error contacting the server (Error: {str(e)})."

        # If 200, try to extract the assistant text robustly
        if response.status_code == 200:
            try:
                result = response.json()
            except ValueError:
                # Invalid JSON
                return "I'm here to listen. I got an unexpected response from the server."

            # Typical OpenAI-style / OpenRouter responses may have choices[] -> message -> content
            # Try several safe access patterns
            try:
                # Preferred: choices[0].message.content
                content = result["choices"][0]["message"]["content"]
            except Exception:
                # Try fallback: choices[0].text
                try:
                    content = result["choices"][0].get("text")
                except Exception:
                    content = None

            if content:
                return content.strip()
            else:
                # If no content found, return helpful debugging info (short)
                # Do not expose sensitive info; show limited details
                debug_snippet = str(result)[:350]
                return f"I'm here to listen. The assistant returned an unexpected response. ({debug_snippet})"

        # Non-200 responses: include code for debugging but keep user-facing message friendly
        else:
            # Attempt to get server error details without leaking secrets
            details = ""
            try:
                # response.text may be large; keep a short preview
                details = response.text[:400]
            except Exception:
                details = "no details available"

            # Log details to Streamlit app logs for maintainer (optional)
            st.error(f"OpenRouter API call failed: status={response.status_code}, details={details}")

            if response.status_code == 401:
                return "I'm here to listen. The AI service rejected our credentials (Unauthorized). Please check the API key."
            elif response.status_code == 429:
                return "I'm here to listen. The service is rate-limited right now. Please try again in a moment."
            else:
                return f"I'm here to listen. Something went wrong (Status: {response.status_code})."

# create global instance (optional)
openrouter_client = OpenRouterClient()
