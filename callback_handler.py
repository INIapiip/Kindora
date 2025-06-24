# callback_handler.py
import time
from typing import Any, Dict, List
import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler

class GeminiCallbackHandler(BaseCallbackHandler):
    def __init__(self, max_update_rate: float = 0.3):
        self.response = ""
        self.last_update = time.time()
        self.last_token_time = time.time()
        self.container = st.empty()
        self.max_update_rate = max_update_rate
        self.token_count = 0
        
    def on_llm_start(self, serialized: Dict[str, Any], 
                    prompts: List[str], **kwargs: Any) -> None:
        """Sederhanakan animasi loading"""
        with self.container:
            st.markdown("⚠️ <i>Mempersiapkan respon...</i>", unsafe_allow_html=True)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Optimasi update rate dengan dynamic delay"""
        self.response += token
        self.token_count += 1
        
        current_time = time.time()
        elapsed = current_time - self.last_update
        
        # Dynamic update rate berdasarkan panjang token
        dynamic_delay = max(
            self.max_update_rate, 
            0.5 - min(self.token_count * 0.01, 0.4)  # Lebih cepat saat token banyak
        )
        
        if elapsed >= dynamic_delay:
            self._update_display(False)
            self.last_update = current_time
            self.last_token_time = current_time

    def on_llm_end(self, response, **kwargs: Any) -> None:
        """Handle response kosong"""
        if not self.response.strip():
            self.response = "Maaf, saya tidak mendapat respon yang valid."
        self._update_display(True)
        
    def _update_display(self, final: bool):
        """Format yang lebih bersih dengan batasan panjang"""
        truncated = (self.response[:200] + '...') if len(self.response) > 200 else self.response
        
        with self.container:
            if final:
                st.markdown(f"""
                <div class='assistant-response'>
                    <div class='response-header'>💡 Respon</div>
                    <div class='response-content'>{truncated}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                cursor = "▌" if (time.time() - self.last_token_time) < 0.5 else "&nbsp;"
                st.markdown(f"""
                <div class='assistant-response'>
                    <div class='response-header'>🔄 Memproses</div>
                    <div class='response-content'>{truncated}{cursor}</div>
                </div>
                """, unsafe_allow_html=True)
