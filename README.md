# 🧠 Kindora - Asisten Kesehatan Mental AI 🇮🇩

Selamat datang di **Kindora**, platform chatbot AI untuk membantu masyarakat Indonesia mendapatkan informasi & rekomendasi terkait kesehatan mental secara cepat, mudah, dan aman.

---

## ✨ Fitur Utama

✅ Chatbot AI interaktif untuk menjawab pertanyaan seputar kesehatan mental
✅ Upload dokumen PDF, sistem akan membantu membaca & menjelaskan isinya
✅ Pencarian informasi terbaru menggunakan Google Search
✅ Rekomendasi kesehatan mental berbasis database internal
✅ Mendukung beberapa model AI seperti Gemini dan Mistral
✅ Tampilan modern dengan Streamlit & custom CSS yang nyaman dilihat

---

## 🚀 Cara Instalasi

**1. Clone Repository**

```bash
git clone https://github.com/INIapiip/Kindora.git
cd Kindora
```

**2. Install Dependencies**
Pastikan sudah ada Python minimal 3.9

```bash
pip install -r requirements.txt
```

**3. Setup API Key**

* Buat file `.env` (tidak termasuk repo, sudah di `.gitignore`)
* Isi dengan:

```bash
COHERE_API_KEY=xxx
GOOGLE_CSE_ID=xxx
GOOGLE_API_KEY=xxx
```

Atau bisa input langsung API Key Gemini saat menjalankan aplikasi melalui sidebar.

**4. Jalankan Aplikasi**

```bash
streamlit run main.py
```

---

## 💡 Teknologi yang Digunakan

* [Streamlit](https://streamlit.io) → UI web interaktif
* [Langchain](https://python.langchain.com/) → Integrasi LLM & tool eksternal
* [Google Generative AI (Gemini)](https://ai.google.dev/) → Model AI untuk respons cerdas
* [FAISS](https://github.com/facebookresearch/faiss) → Penyimpanan & pencarian vektor database
* [Cohere Embeddings](https://docs.cohere.com/) → Representasi teks berbasis AI
* Google Search API untuk pencarian eksternal terkini

---

## 🎨 Preview Tampilan

| Chat Bot                                                             | Upload PDF                                                         |
| -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| ![chat](https://github.com/INIapiip/Kindora/assets/preview_chat.png) | ![pdf](https://github.com/INIapiip/Kindora/assets/preview_pdf.png) |

---

## 🛠 Struktur Folder

```
Kindora/
├── data/               # Database FAISS
├── tools/              # Modular tools chatbot
├── mental_health_processor.py  # Ekstrak teks PDF
├── retriever.py        # Inisialisasi FAISS retriever
├── style.css           # Tampilan kustom
├── main.py             # Streamlit app utama
├── create_index.py     # Buat index FAISS dari data
├── rag.py              # Retrieval-Augmented Generation opsional
├── callback_handler.py # Logging & monitoring LLM
├── requirements.txt    # Dependencies
```

---

## ⚠️ Catatan

❗ `.env` bersifat privat, simpan baik-baik kunci API Anda
❗ Project ini hanya memberikan informasi & rekomendasi, bukan pengganti konsultasi profesional

---

## 🤝 Kontribusi

Pull request & feedback sangat diterima!
Silakan fork, buka issue, atau kontak langsung via GitHub.

---

## ❤️ Dukungan

Project ini dibuat sebagai kontribusi untuk meningkatkan kesadaran & akses informasi kesehatan mental di Indonesia.

**Mari bersama-sama peduli kesehatan mental!**
