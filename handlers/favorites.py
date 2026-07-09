from telegram import Update
from telegram.ext import ContextTypes
from services.database import get_favorites, add_favorite, remove_favorite
from keyboards.inline import get_favorites_management_keyboard

async def favorites_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    favs = await get_favorites(user_id)
    await update.message.reply_text(
        "⭐️ **Manage Favorite Languages**\nSelect items to toggle addition/removal from your quick-access panel:",
        reply_markup=get_favorites_management_keyboard(favs),
        parse_mode="Markdown"
    )

async def favorites_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data
    
    if data == "close_favorites":
        await query.message.edit_text("⭐️ Settings updated successfully.")
        return
        
    lang_code = data.split("_")[1]
    favs = await get_favorites(user_id)
    
    if lang_code in favs:
        await remove_favorite(user_id, lang_code)
    else:
        await add_favorite(user_id, lang_code)
        
    updated_favs = await get_favorites(user_id)
    await query.message.edit_reply_markup(reply_markup=get_favorites_management_keyboard(updated_favs))
