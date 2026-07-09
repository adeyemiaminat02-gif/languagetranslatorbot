from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_language_keyboard, get_shortcut_keyboard
from services.database import get_user_last_lang, update_last_lang, add_history, get_favorites
from services.translator import translate_text, ALL_LANGUAGES
from utils.logger import logger

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text_to_translate = update.message.text
    if text_to_translate.startswith('/'):
        return
        
    if len(text_to_translate) > 2000:
        await update.message.reply_text("⚠️ Message too long. Please restrict text inputs to 2000 characters.")
        return

    context.user_data['text_to_translate'] = text_to_translate
    user_id = update.effective_user.id
    last_code = await get_user_last_lang(user_id)
    
    last_name = ALL_LANGUAGES.get(last_code, "English")
    await update.message.reply_text(
        f"Received your text. Target language options:",
        reply_markup=get_shortcut_keyboard(last_code, last_name)
    )

async def process_translation_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    favs = await get_favorites(user_id)
    await query.message.edit_text(
        "Select your destination language:",
        reply_markup=get_language_keyboard("popular", favorites=favs)
    )

async def language_page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = query.data.split("_")[1]
    user_id = query.from_user.id
    favs = await get_favorites(user_id)
    await query.message.edit_reply_markup(reply_markup=get_language_keyboard(page, favorites=favs))

async def translation_execution_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    target_lang = query.data.split("_")[1]
    user_id = query.from_user.id
    
    text = context.user_data.get('text_to_translate')
    if not text:
        await query.message.edit_text("❌ Session timed out or text context empty. Please send text again.")
        return

    await query.message.edit_text("🔄 Processing high-fidelity translation...")
    
    try:
        translated = await translate_text(text, target_lang)
        await update_last_lang(user_id, target_lang)
        await add_history(user_id, text, translated, target_lang)
        
        target_lang_name = ALL_LANGUAGES.get(target_lang, target_lang.upper())
        response = (
            f"🌐 **Translation Complete**\n\n"
            f"**Original Text:**\n`{text}`\n\n"
            f"**Translated ({target_lang_name}):**\n`{translated}`"
        )
        await query.message.edit_text(response, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Execution Error: {e}")
        await query.message.edit_text("💥 Connection Timeout or API error. Please try again shortly.")
