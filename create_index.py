# ✅ create_index.py (VERSI FINAL, TANPA ERROR)
# Membuat FAISS index dari CSV dengan Cohere + LangChain + User-Agent aman

import os
import shutil
import pandas as pd
import cohere
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

def create_faiss_index():
    load_dotenv()

    # ✅ Set user agent via ENV (bukan di parameter)
    os.environ["LANGCHAIN_USER_AGENT"] = "mental-health-chatbot"

    # Path ke file dan index
    csv_path = "data/Mental_Health_FAQ.csv"
    index_dir = "data/faiss_index"

    # Validasi file CSV
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ File CSV tidak ditemukan: {csv_path}")

    # Hapus index lama jika ada
    if os.path.exists(index_dir):
        shutil.rmtree(index_dir)
    os.makedirs(index_dir, exist_ok=True)

    # Ambil API Key
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("❌ COHERE_API_KEY tidak ditemukan di file .env")

    # Baca dan gabungkan data
    df = pd.read_csv(csv_path).fillna("")
    df["combined"] = df.astype(str).agg(" ".join, axis=1)
    docs = [Document(page_content=text) for text in df["combined"].tolist()]

    # Split teks jadi chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    # Embeddings & vectorstore
    cohere_client = cohere.Client(api_key=cohere_api_key)
    embeddings = CohereEmbeddings(
        client=cohere_client,
        model="embed-multilingual-v3.0",  # ✅ WAJIB
        async_client=None
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_dir)

    print(f"✅ FAISS index berhasil disimpan ke folder: {index_dir}")

if __name__ == "__main__":
    create_faiss_index()
