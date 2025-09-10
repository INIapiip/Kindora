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
        css_content = f.read()
        css_content += """
        section[data-testid="stSidebar"] {
            background-color: #bb377d;
        }
        """
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
        st.markdown("<div class='bg-animation'></div>", unsafe_allow_html=True)

def get_google_search_results(query: str) -> str:
    try:
        num_results = 10
        results = list(search(query, num_results=num_results, lang="id"))
        if not results:
            return f"Maaf, saya tidak dapat menemukan hasil yang relevan di Google untuk '{query}'."

        url_list = "\n".join([f"{i+1}. {url}" for i, url in enumerate(results)])
        return (
            f"Berikut hasil pencarian untuk '{query}':\n{url_list}\n\n"
            "**Catatan:** Harap evaluasi kredibilitas situs secara mandiri."
        )
    except Exception as e:
        return f"Kesalahan saat pencarian Google: {str(e)}"

def run_agent(user_input: str, retriever: FaissRetriever, pdf_content: Optional[str] = None) -> str:
    system_prompt = ""
    if pdf_content:
        system_prompt = f"""
        PERHATIAN: Pengguna mengunggah dokumen. Jawab HANYA berdasarkan:
        --- DOKUMEN ---
        {pdf_content}
        --- AKHIR DOKUMEN ---
        """

    tools = [
        Tool(name='cari_info_kesehatan_mental', func=lambda q: get_professional_help(q, retriever), description="Jawab spesifik dari database."),
        Tool(name='beri_rekomendasi_kesehatan_mental', func=lambda q: get_coping_tips(), description="Rekomendasi coping."),
        Tool(name='pencarian_internet_google', func=search, description="Cari info baru."),
        Tool(name='terjemah_bahasa', func=TranslationService, description="Terjemahkan."),
        Tool(name='dapatkan_tanggal_sekarang', func=show_current_date, description="Tanggal saat ini.")
    ]

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=st.session_state.gemini_api_key,
        temperature=0.2,
        callbacks=[GeminiCallbackHandler()],
        convert_system_message_to_human=True
    )

    if pdf_content:
        prompt = f"""
        Kamu adalah asisten kesehatan mental. Jawab berdasarkan dokumen berikut:
        --- DOKUMEN ---
        {pdf_content}
        --- AKHIR DOKUMEN ---
        Pertanyaan: {user_input}
        """
        return str(llm.invoke(prompt).content)

    retriever_result = retriever.search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in retriever_result]) if retriever_result else ""

    if context.strip():
        prompt = f"""
        Kamu adalah asisten kesehatan mental. Jawab berdasarkan database berikut:
        --- DATABASE ---
        {context}
        --- AKHIR DATABASE ---
        Pertanyaan: {user_input}
        """
        return str(llm.invoke(prompt).content)

    st.info("🔍 Tidak ada jawaban di database. Mencoba dari internet...")
    return get_google_search_results(user_input)

def main():
    st.set_page_config(page_title="Kindora Mental Health", page_icon="🧠", layout="centered")
    load_css()

    if "user_name" not in st.session_state or "gemini_api_key" not in st.session_state:
        st.markdown("""
        <div class='header'>
            <h1>💖 Selamat Datang di Kindora Chatbot</h1>
            <p>Isi Nama & API Key dulu yuk~</p>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("Nama Kamu 💫")

        if st.button("Mulai Chat 💖"):
            if name.strip() and api_key.strip():
                st.session_state.user_name = name.strip()
                st.session_state.gemini_api_key = api_key.strip()
                st.rerun()
            else:
                st.warning("Nama dan API Key wajib diisi.")
        return

    st.markdown(f"""
    <div class='header'>
        <h1>💖 Hai {st.session_state.user_name}!</h1>
        <p>Senang bisa ngobrol bareng kamu ✨</p>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Halo! Cerita apa hari ini?"}]
    if "pdf_content" not in st.session_state:
        st.session_state.pdf_content = None
    if "retriever" not in st.session_state:
        st.session_state.retriever = FaissRetriever(index_path="data/faiss_index")

    with st.sidebar:
        st.header(f"📜 Riwayat {st.session_state.user_name}")
        if st.session_state.messages:
            for msg in st.session_state.messages:
                if msg["role"] != "system":
                    label = "👤 Kamu" if msg["role"] == "user" else "🤖 AI"
                    isi = msg["content"][:40] + "..." if len(msg["content"]) > 40 else msg["content"]
                    st.write(f"{label}: {isi}")
        else:
            st.info("Belum ada percakapan.")

        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Riwayat dihapus. Yuk mulai lagi."}]
            st.session_state.pdf_content = None
            st.success("Riwayat berhasil dihapus.")

        st.divider()
        uploaded_file = st.file_uploader("📄 Upload PDF (Opsional)", type=["pdf"])
        if uploaded_file:
            with st.spinner("Membaca dokumen..."):
                hasil = extract_mental_health_document(uploaded_file)
                if 'error' in hasil:
                    st.error(hasil['error'])
                else:
                    st.session_state.pdf_content = hasil['full_text']
                    st.success("Dokumen berhasil diproses!")

    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🧠"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Tanyakan sesuatu..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Asisten sedang berpikir..."):
                response = run_agent(user_input, st.session_state.retriever, st.session_state.pdf_content)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response)

if __name__ == "__main__":
    main()
