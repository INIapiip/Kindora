# mental_health_chatbot/mental_health_processor.py
import PyPDF2
import pdfplumber
from typing import Dict, Union
import re
import io

class MentalHealthDocumentProcessor:
    """Processor khusus untuk dokumen kesehatan mental (PDF)"""
    
    def __init__(self):
        self.mental_health_keywords = [
            'mental health', 'depression', 'anxiety', 'stress', 
            'psikologis', 'depresi', 'kecemasan', 'gangguan mood',
            'terapi', 'konseling', 'skrining', 'diagnosis', 'DSM-5'
        ]

    def extract_text_from_pdf(self, file_stream) -> Dict[str, Union[str, dict]]:
        """Ekstrak teks dari PDF dengan prioritas konten kesehatan mental"""
        try:
            # Coba dengan pdfplumber terlebih dahulu untuk presisi
            with pdfplumber.open(file_stream) as pdf:
                full_text = ""
                mental_health_pages = {}
                
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                        
                        # Deteksi halaman relevan
                        if self._is_mental_health_content(page_text):
                            mental_health_pages[i+1] = self._summarize_page(page_text)
                
                # Jika menemukan konten spesifik kesehatan mental
                if mental_health_pages:
                    highlighted_content = self._highlight_keywords(full_text)
                    return {
                        'status': 'success',
                        'full_text': full_text,
                        'mental_health_pages': mental_health_pages,
                        'highlighted_content': highlighted_content,
                        'summary': self._generate_summary(full_text)
                    }
                else:
                    return {
                        'status': 'success',
                        'full_text': full_text,
                        'summary': self._generate_summary(full_text)
                    }

        except Exception as pdfplumber_error:
            print(f"pdfplumber error: {pdfplumber_error}, trying PyPDF2...")
            try:
                # Fallback ke PyPDF2
                file_stream.seek(0)
                pdf_reader = PyPDF2.PdfReader(file_stream)
                full_text = ""
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                
                return {
                    'status': 'success',
                    'full_text': full_text,
                    'summary': self._generate_summary(full_text)
                }
                
            except Exception as e:
                return {
                    'status': 'error',
                    'error': f"Gagal memproses PDF: {str(e)}"
                }

    def _is_mental_health_content(self, text: str) -> bool:
        """Deteksi apakah teks mengandung konten kesehatan mental"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.mental_health_keywords)

    def _highlight_keywords(self, text: str) -> str:
        """Highlight keyword kesehatan mental dalam teks"""
        highlighted = text
        for keyword in self.mental_health_keywords:
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            highlighted = pattern.sub(f"**{keyword.upper()}**", highlighted)
        return highlighted

    def _summarize_page(self, page_text: str) -> str:
        """Ringkas halaman yang relevan"""
        sentences = re.split(r'(?<=[.!?])\s+', page_text)
        relevant_sentences = [
            s for s in sentences 
            if any(keyword.lower() in s.lower() for keyword in self.mental_health_keywords)
        ]
        return " ".join(relevant_sentences[:3]) + "..." if relevant_sentences else ""

    def _generate_summary(self, text: str) -> str:
        """Buat ringkasan dokumen yang fokus pada aspek kesehatan mental"""
        paragraphs = [p for p in text.split('\n') if p.strip()]
        relevant_paras = [
            p for p in paragraphs 
            if self._is_mental_health_content(p)
        ][:3]
        
        if not relevant_paras:
            return "Dokumen ini tidak memiliki konten kesehatan mental yang terdeteksi."
        
        return "\n\n".join([
            "DOKUMEN MENGANDUNG INFORMASI TENTANG:",
            "- " + "\n- ".join([
                para[:150] + "..." if len(para) > 150 else para 
                for para in relevant_paras
            ]),
            "\nGunakan fitur chat untuk bertanya spesifik tentang dokumen ini."
        ])

# Fungsi untuk kompatibilitas dengan Streamlit
def extract_mental_health_document(uploaded_file):
    processor = MentalHealthDocumentProcessor()
    file_stream = io.BytesIO(uploaded_file.read())
    return processor.extract_text_from_pdf(file_stream)
