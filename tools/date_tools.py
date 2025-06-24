# mental_health_chatbot/tools/date_tool.py
import streamlit as st
from datetime import datetime

def show_current_date():
    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    st.session_state.message.append({
        "role": "assistant", 
        "content": f"Today is {current_date}"
    })
    st.rerun()
