# mental_health_chatbot/tools/coping_tool.py
import streamlit as st

COPING_TIPS = [
    "Practice deep breathing: Inhale for 4 seconds, hold for 7, exhale for 8",
    "Try grounding techniques: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste",
    "Go for a short walk outside to clear your mind",
    "Write down your thoughts in a journal",
    "Listen to calming music or nature sounds"
]

def get_coping_tips():
    tip = st.session_state.messages.append({
        "role": "assistant",
        "content": "Here are some coping strategies you can try:\n\n" + 
                   "\n".join(f"• {tip}" for tip in COPING_TIPS)
    })
    st.rerun()
