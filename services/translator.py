from deep_translator import GoogleTranslator
from utils.logger import logger

POPULAR_LANGUAGES = {
    'en': 'English', 'fr': 'French', 'es': 'Spanish', 'de': 'German',
    'pt': 'Portuguese', 'it': 'Italian', 'ar': 'Arabic', 'zh-CN': 'Chinese',
    'ja': 'Japanese', 'ko': 'Korean', 'hi': 'Hindi', 'ru': 'Russian',
    'tr': 'Turkish'
}

EXTENDED_LANGUAGES = {
    'nl': 'Dutch', 'el': 'Greek', 'he': 'Hebrew', 'id': 'Indonesian',
    'pl': 'Polish', 'sv': 'Swedish', 'vi': 'Vietnamese', 'th': 'Thai'
}

ALL_LANGUAGES = {**POPULAR_LANGUAGES, **EXTENDED_LANGUAGES}

async def translate_text(text: str, target_lang: str):
    try:
        # GoogleTranslator auto-detects source language natively
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated = translator.translate(text)
        return translated
    except Exception as e:
        logger.error(f"Translation API error: {e}")
        raise e
