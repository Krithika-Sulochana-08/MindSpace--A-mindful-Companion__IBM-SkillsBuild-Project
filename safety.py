import re

CRISIS_KEYWORDS = [
    'suicide', 'kill myself', 'end it all', 'want to die', 'not worth living',
    'harm myself', 'self harm', 'hurt myself', 'better off dead', 'no way out',
    'ending it', 'suicidal', 'want to disappear', 'can\'t go on', 'give up',
    'end my life', 'don\'t want to live', 'tired of living'
]

def contains_crisis_keywords(text):
    """Check if text contains crisis-related keywords"""
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in CRISIS_KEYWORDS)

def validate_input(text):
    """Basic input validation"""
    if not text or len(text.strip()) == 0:
        return False, "Please enter a message"
    
    if len(text) > 1000:
        return False, "Message too long. Please keep under 1000 characters"
    
    return True, ""

def get_crisis_resources():
    """Return crisis resources information for INDIA"""
    return {
        "emergency": "108 or 112 (National Emergency Number)",
        "vandrevala": "080-46110007 (Vandrevala Foundation)",
        "icall": "9152987821 (iCall Psychosocial Helpline)",
        "sneha": "044-24640050 (SNEHA Suicide Prevention)",
        "warning": "If you're in immediate danger, please contact emergency services right away."
    }