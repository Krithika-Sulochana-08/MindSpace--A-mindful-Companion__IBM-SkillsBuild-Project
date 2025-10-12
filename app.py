import streamlit as st
from datetime import datetime
import pandas as pd
from openrouter_client import openrouter_client
from utils.prompts import COPING_STRATEGIES, MOOD_QUESTIONS, WELLNESS_TIPS
from utils.safety import contains_crisis_keywords, validate_input, get_crisis_resources

# Page configuration
st.set_page_config(
    page_title="MindSpace: A Mindful Companion",
    page_icon="💭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        line-height: 1.6;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #4A90E2;
    }
    .assistant-message {
        background-color: #F5F5F5;
        border-left: 4px solid #66BB6A;
    }
    .crisis-alert {
        background-color: #FFEBEE;
        border: 2px solid #F44336;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .resource-box {
        background-color: #E8F5E8;
        border: 1px solid #66BB6A;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .tip-box {
        background-color: #E3F2FD;
        border: 1px solid #2196F3;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


class MentalHealthCompanion:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'mood_log' not in st.session_state:
            st.session_state.mood_log = []
        if 'coping_used' not in st.session_state:
            st.session_state.coping_used = []
        if 'conversation_started' not in st.session_state:
            st.session_state.conversation_started = False
    
    def get_ai_response(self, user_input):
        """Get response from OpenRouter"""
        try:
            response = openrouter_client.generate_response(user_input)
            return response
        except Exception:
            return "I'm having trouble connecting right now. Please try again later."
    
    def log_mood(self, mood, notes=""):
        """Log user's mood with auto-calculated intensity"""
        mood_intensity_map = {
            "😢 Very Low": 2,
            "😞 Low": 4,
            "😐 Okay": 6,
            "😊 Good": 8,
            "🎉 Great": 10
        }
        
        intensity = mood_intensity_map.get(mood, 5)
        
        st.session_state.mood_log.append({
            'timestamp': datetime.now(),
            'mood': mood,
            'intensity': intensity,
            'notes': notes
        })
    
    def add_coping_strategy(self, strategy):
        """Add coping strategy to used list"""
        if strategy not in [entry['strategy'] for entry in st.session_state.coping_used]:
            st.session_state.coping_used.append({
                'strategy': strategy,
                'timestamp': datetime.now()
            })


def main():
    companion = MentalHealthCompanion()
    
    # Header
    st.markdown('<h1 class="main-header">🧠 MindSpace: A Mindful Companion</h1>', unsafe_allow_html=True)
    st.markdown("### Your AI Mental Health Support Partner")
    
    # Sidebar
    with st.sidebar:
        st.header("🌱 Wellness Tools")
        
        # Mood Tracker
        st.subheader("Mood Tracker")
        mood = st.select_slider("How are you feeling today?", 
                               options=["😢 Very Low", "😞 Low", "😐 Okay", "😊 Good", "🎉 Great"])
        mood_notes = st.text_area("Brief notes (optional):", placeholder="What's contributing to this mood?", height=60)
        
        if st.button("Log Mood", use_container_width=True):
            companion.log_mood(mood, mood_notes)
            st.success("Mood logged!")
    
        # Coping Strategies
        st.subheader("Coping Strategies")
        selected_strategy = st.selectbox("Choose a strategy:", COPING_STRATEGIES)
        if st.button("Use This Strategy", use_container_width=True):
            companion.add_coping_strategy(selected_strategy)
            st.info(f"💡 {selected_strategy}")
        
        # Conversation starters
        st.subheader("Need a starting point?")
        if not st.session_state.conversation_started:
            for i, question in enumerate(MOOD_QUESTIONS[:3]):
                if st.button(question, key=f"starter_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": question})
                    st.session_state.conversation_started = True
                    st.rerun()
        
        # Crisis Resources
        st.subheader("🆘 Crisis Resources (India)")
        resources = get_crisis_resources()
        st.write(f"**{resources['emergency']}**")
        st.write(f"**{resources['vandrevala']}**")
        st.write(f"**{resources['icall']}**")
        
        # Clear Chat
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()

    # Main chat section
    st.header("💬 Talk with Your Companion")
    
    # Crisis alert check
    crisis_detected = any(
        contains_crisis_keywords(msg.get('content', '')) 
        for msg in st.session_state.messages if msg.get('role') == 'user'
    )
    
    if crisis_detected:
        st.markdown("""
        <div class="crisis-alert">
            <h3>🚨 Your Safety is Important</h3>
            <p>If you're experiencing thoughts of harming yourself, please contact professional help immediately:</p>
            <ul>
                <li><strong>108 or 112</strong> - National Emergency Services</li>
                <li><strong>080-46110007</strong> - Vandrevala Foundation Helpline (24/7)</li>
                <li><strong>9152987821</strong> - iCall Psychosocial Helpline</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>Companion:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Welcome message for first-time users
    if not st.session_state.messages:
        st.markdown("""
        <div class="chat-message assistant-message">
            <strong>Companion:</strong><br>
            Hello! I'm here to listen and support you. This is a safe space where you can share whatever's on your mind — 
            your feelings, concerns, or anything you'd like to talk about. I'm here to provide 
            compassionate, non-judgmental support.
            <br><br><em>What would you like to talk about today?</em>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input box
    user_input = st.chat_input("Share what's on your mind...")
    
    if user_input:
        # Validate input
        is_valid, validation_msg = validate_input(user_input)
        if not is_valid:
            st.error(validation_msg)
        else:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.conversation_started = True
            
            # Get AI response
            with st.spinner("💭 Companion is thinking..."):
                response = companion.get_ai_response(user_input)
            
            # Add AI response
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    # Wellness tools below chat
    st.markdown("---")
    st.header("📊 Your Wellness Journey")
    
    col1, col2 = st.columns(2)
    
    # ✅ Mood History (Graph Removed — Summary only)
    with col1:
        st.subheader("Mood History")
        if st.session_state.mood_log:
            num_entries = len(st.session_state.mood_log)
            most_recent = st.session_state.mood_log[-1]
            st.markdown(f"**Mood entries logged:** {num_entries}")
            st.markdown(f"**Most recent:** {most_recent['mood']} ({most_recent['intensity']}/10)")
            if most_recent.get('notes'):
                st.caption(f"*{most_recent['notes']}*")
            
            st.subheader("Recent Check-ins")
            for entry in reversed(st.session_state.mood_log[-3:]):
                st.write(f"**{entry['mood']}** ({entry['intensity']}/10) — {entry['timestamp'].strftime('%b %d %H:%M')}")
                if entry.get('notes'):
                    st.caption(f"*{entry['notes']}*")
        else:
            st.write("No mood entries yet. Log your mood using the Mood Tracker on the left.")
    
    with col2:
        # Coping Strategies used
        if st.session_state.coping_used:
            st.subheader("Recently Used Strategies")
            for entry in reversed(st.session_state.coping_used[-3:]):
                st.write(f"• {entry['strategy']}")
        
        # Quick Wellness Tips
        st.subheader("💡 Quick Wellness Tips")
        for tip in WELLNESS_TIPS[:4]:
            st.markdown(f'<div class="tip-box">{tip}</div>', unsafe_allow_html=True)
        
        # Emergency resources
        st.markdown("""
        <div class="resource-box">
            <h4>🆘 Immediate Help Available (India)</h4>
            <p><strong>108 or 112</strong> - National Emergency Services<br>
            <strong>080-46110007</strong> - Vandrevala Foundation<br>
            <strong>9152987821</strong> - iCall Helpline</p>
        </div>
        """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        <p><strong>Disclaimer:</strong> This AI companion offers supportive listening only. 
        It is not a substitute for professional medical or psychological help. 
        If you're in crisis, please contact a licensed professional or emergency services.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
