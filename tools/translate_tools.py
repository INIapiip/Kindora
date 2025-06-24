from deep_translator import GoogleTranslator
from time import sleep
import random

class TranslationService:
    MAX_RETRIES = 3
    BASE_DELAY = 1.5

    @staticmethod
    def translate_to_indonesian(text: str) -> str:
        return TranslationService._translate(text, target='id')

    @staticmethod
    def translate_to_english(text: str) -> str:
        return TranslationService._translate(text, target='en')

    @staticmethod
    def _translate(text: str, target: str) -> str:
        if not text:
            return ""
        
        for attempt in range(TranslationService.MAX_RETRIES):
            try:
                # Translate using Google Translator
                translated_text = GoogleTranslator(target=target).translate(text)
                sleep(random.uniform(TranslationService.BASE_DELAY, TranslationService.BASE_DELAY * 2))
                return translated_text
            except Exception as e:
                print(f"Translation failed on attempt {attempt + 1}: {e}")
                sleep(TranslationService.BASE_DELAY)
        return "Translation failed after multiple attempts."
