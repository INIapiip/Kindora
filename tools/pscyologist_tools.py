# mental_health_chatbot/tools/pscyologist_tools.py
import streamlit as st

# ✅ 1. TAMBAHKAN DEFINISI VARIABEL INI (sebelum digunakan)
PROFESSIONAL_RESOURCES = [
    "Indonesian Psychological Association (HIMPSI): https://himpsi.or.id",
    "Into The Light Indonesia (Suicide Prevention): https://intothelightidn.org",
    "PULIH Foundation: http://pulih.or.id",
    "Jakarta Counseling Center: https://jakartacounselingcenter.com",
    "Emergency contact: 119 (Indonesian mental health emergency number)"
]

# ✅ 2. PERBAIKI FUNGSI (sesuaikan parameter)
def get_professional_help(query=None, retriever=None):
    """
    Memberikan sumber bantuan profesional kesehatan mental.
    
    Args:
        query (str, optional): Pertanyaan spesifik dari user untuk pencarian FAISS
        retriever (FaissRetriever, optional): Objek retriever untuk search
    
    Returns:
        str: Daftar sumber bantuan dalam format teks
    """
    if query and retriever:  # Jika ada query & retriever, gunakan vector search
        try:
            results = retriever.search(query, k=3)
            if results:
                return "\n".join(f"• {res.page_content}" for res in results)
        except Exception as e:
            st.error(f"Error saat mencari: {str(e)}")
            return "Gagal mencari data. Menampilkan daftar default..."
    
    # Fallback ke daftar default jika search gagal/tidak ada parameter
    return "Berikut beberapa sumber bantuan profesional:\n\n" + "\n".join(f"• {res}" for res in PROFESSIONAL_RESOURCES)

# ✅ 3. TEST FUNCTION (opsional)
if __name__ == "__main__":
    print(get_professional_help())  # Test tanpa parameter
    print(get_professional_help("depression"))  # Test dengan query
