# File utama aplikasi Chatbot Kesehatan Mental AI

import os
from dotenv import load_dotenv
import streamlit as st
import datetime
# Import library LangChain dan lainnya
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import GoogleAPICallError
from googlesearch import search
from typing import Optional
from langchain_cohere import CohereEmbeddings

# Import komponen lokal
from retriever import FaissRetriever
from mental_health_processor import extract_mental_health_document
from callback_handler import GeminiCallbackHandler

# Import semua fungsi dari tools
from tools.date_tools import show_current_date
from tools.cooping_tools import get_coping_tips
from tools.pscyologist_tools import get_professional_help
from tools.save_history import save_chat_history
from tools.translate_tools import TranslationService

load_dotenv()

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_google_search_results(query: str) -> str:
    try:
        results = list(search(query, num_results=10, lang="id"))
        if not results:
            return "Maaf, saya tidak menemukan hasil di Google."
        return "\n".join([f"{i+1}. {url}" for i, url in enumerate(results)])
    except Exception as e:
        return f"Kesalahan saat mencari: {str(e)}"

def run_agent(user_input: str, retriever: FaissRetriever, pdf_content: Optional[str] = None) -> str:
    system_prompt = f"""PERHATIAN: Jika ada dokumen, jawab hanya berdasarkan dokumen di bawah:
---
{pdf_content or 'Tidak ada dokumen'}
---"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=st.session_state.gemini_api_key,
        temperature=0.2,
        callbacks=[GeminiCallbackHandler()],
        convert_system_message_to_human=True
    )

    retriever_result = retriever.search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in retriever_result])

    if context.strip():
        prompt = f"{system_prompt}\nDATA:\n{context}\nPertanyaan: {user_input}"
    else:
        return get_google_search_results(user_input)

    return str(llm.invoke(prompt).content)

def main():
    st.set_page_config(page_title="Kindora Chatbot", page_icon="🧠", layout="centered")
    load_css()

    if "user_name" not in st.session_state or "gemini_api_key" not in st.session_state:
        st.markdown("""
        <div class='header'>
            <h1>💖 Selamat Datang di Kindora</h1>
            <p>Masukkan Nama & API Key dulu ya~</p>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Nama Kamu 💫")
        api_key = st.text_input("API Token Gemini 🔑", type="password")

        if st.button("Mulai Chat 💖") and name.strip() and api_key.strip():
            st.session_state.user_name = name.strip()
            st.session_state.gemini_api_key = api_key.strip()
            st.rerun()
        return

    st.markdown(f"""
    <div class='header'>
        <h1>💖 Hai {st.session_state.user_name}!</h1>
        <p>Cerita apa hari ini? ✨</p>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Halo! Aku Kindora, siap dengerin ceritamu."}]
    if "pdf_content" not in st.session_state:
        st.session_state.pdf_content = None
    if "retriever" not in st.session_state:
        st.session_state.retriever = FaissRetriever(index_path="data/faiss_index")

    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🧠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Tulis ceritamu atau pertanyaan..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Kindora lagi mikir..."):
                response = run_agent(user_input, st.session_state.retriever, st.session_state.pdf_content)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response)

    st.divider()
    with st.expander("📝 Riwayat Percakapan"):
        for msg in st.session_state.messages:
            siapa = "Kamu" if msg["role"] == "user" else "Kindora"
            st.write(f"**{siapa}:** {msg['content']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Riwayat sudah dihapus. Yuk mulai lagi!"}]
            st.success("Riwayat terhapus.")

    with col2:
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
        st.caption("📄 Upload Dokumen PDF")
        if uploaded_file:
            with st.spinner("Membaca dokumen..."):
                result = extract_mental_health_document(uploaded_file)
                if 'error' in result:
                    st.error(result['error'])
                else:
                    st.session_state.pdf_content = result['full_text']
                    st.success("Dokumen berhasil diproses!")

if __name__ == "__main__":
    main()
