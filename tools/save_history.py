# mental_health_chatbot/tools/save_history_tool.py
import json
from datetime import datetime

def save_chat_history(messages):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")
