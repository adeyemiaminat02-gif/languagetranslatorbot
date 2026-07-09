from telegram import Update
from telegram.ext import ContextTypes
from keyboards.inline import get_start_keyboard
from services.database import add_user

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await add_user(user.id, user.username)
    await update.message.reply_text(
        f"Welcome {user.first_name} to @TheLanguageTranslatorBot!\n\n"
        f"I can automatically detect any language you send and translate it to your choice.\n"
        f"Tap the button below or simply send a message to get started.",
        reply_markup=get_start_keyboard()
    )
