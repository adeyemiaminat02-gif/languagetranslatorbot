from telegram import Update
from telegram.ext import ContextTypes
from services.database import get_history

async def history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    history = await get_history(user_id)
    if not history:
        await update.message.reply_text("📜 Your translation history is currently empty.")
        return
    
    text = "📜 **Your Recent Translations (Newest First):**\n\n"
    for idx, (src, trans, lang) in enumerate(history, 1):
        text += f"{idx}. *Original:* {src[:30]}...\n    *→ ({lang.upper()}):* {trans[:40]}\n\n"
    await update.message.reply_text(text, parse_mode="Markdown")
