from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ **How to Use This Bot**\n\n"
        "1. Send any text message directly.\n"
        "2. Choose your destination language via the interactive menu.\n"
        "3. The bot auto-detects your source language!\n\n"
        "**Available Commands:**\n"
        "/start - Welcome screen\n"
        "/history - Show last 10 translations\n"
        "/favorites - Manage shortcut languages\n"
        "/about - Bot deployment details",
        parse_mode="Markdown"
    )
