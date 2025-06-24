# ✅ retriever.py (FINAL AMAN – fix error client/async_client)

import os
from dotenv import load_dotenv
import cohere
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS

class FaissRetriever:
    def __init__(self, index_path: str):
        load_dotenv()

        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("❌ COHERE_API_KEY tidak ditemukan di .env")

        if not os.path.exists(index_path):
            raise FileNotFoundError(f"❌ Index FAISS tidak ditemukan di: {index_path}")

        # Set user agent via environment
        os.environ["LANGCHAIN_USER_AGENT"] = "mental-health-chatbot"

        # ✅ Gunakan client eksplisit (hindari error client/async_client)
        cohere_client = cohere.Client(api_key=cohere_api_key)
        self.embeddings = CohereEmbeddings(
            client=cohere_client,
            model="embed-multilingual-v3.0"
        )

        try:
            self.vectorstore = FAISS.load_local(
                index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            raise RuntimeError(f"Gagal memuat FAISS index: {str(e)}")

    def search(self, query: str, k: int = 3):
        try:
            if not query:
                raise ValueError("Query tidak boleh kosong")
            return self.vectorstore.similarity_search(query, k=k)
        except Exception as e:
            print(f"❌ Error saat mencari: {str(e)}")
            return []

# Contoh penggunaan
if __name__ == '__main__':
    retriever = FaissRetriever(index_path="data/faiss_index")
    hasil = retriever.search("apa penyebab depresi?", k=3)
    for i, doc in enumerate(hasil):
        print(f"\n--- Hasil {i+1} ---\n{doc.page_content[:200]}...")
