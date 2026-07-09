from telegram import Update
from telegram.ext import ContextTypes

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Bot Profile**\n\n"
        "• **Name:** @TheLanguageTranslatorBot\n"
        "• **Version:** 1.0.0\n"
        "• **Engine:** Powered by Deep Engine via Python 3.12\n"
        "• **Framework:** python-telegram-bot v21\n"
        "• **Infrastructure:** Encrypted Production Deployment via Render & SQLite Engine.",
        parse_mode="Markdown"
    )
