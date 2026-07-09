from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from services.translator import POPULAR_LANGUAGES, EXTENDED_LANGUAGES

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 Translate Text", callback_data="action_translate")]
    ])

def get_language_keyboard(page="popular", favorites=None):
    keyboard = []
    langs = POPULAR_LANGUAGES if page == "popular" else EXTENDED_LANGUAGES
    
    if favorites:
        keyboard.append([InlineKeyboardButton("⭐️ Favorites ⭐️", callback_data="ignore")])
        fav_row = []
        for f_code in favorites:
            from services.translator import ALL_LANGUAGES
            if f_code in ALL_LANGUAGES:
                fav_row.append(InlineKeyboardButton(f"⭐ {ALL_LANGUAGES[f_code]}", callback_data=f"lang_{f_code}"))
                if len(fav_row) == 2:
                    keyboard.append(fav_row)
                    fav_row = []
        if fav_row:
            keyboard.append(fav_row)
        keyboard.append([InlineKeyboardButton("-------------------", callback_data="ignore")])

    row = []
    for code, name in langs.items():
        row.append(InlineKeyboardButton(name, callback_data=f"lang_{code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    if page == "popular":
        keyboard.append([InlineKeyboardButton("🌐 More Languages", callback_data="page_extended")])
    else:
        keyboard.append([InlineKeyboardButton("⬅️ Back to Popular", callback_data="page_popular")])
        
    return InlineKeyboardMarkup(keyboard)

def get_shortcut_keyboard(last_lang_code, last_lang_name):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"Yes, translate to {last_lang_name} Again", callback_data=f"lang_{last_lang_code}")],
        [InlineKeyboardButton("Choose Another Language", callback_data="action_translate")]
    ])

def get_favorites_management_keyboard(fav_list):
    from services.translator import ALL_LANGUAGES
    keyboard = []
    for code, name in ALL_LANGUAGES.items():
        status = "❌ Remove" if code in fav_list else "➕ Add"
        keyboard.append([
            InlineKeyboardButton(f"{name}", callback_data="ignore"),
            InlineKeyboardButton(status, callback_data=f"managefav_{code}")
        ])
    keyboard.append([InlineKeyboardButton("Done", callback_data="close_favorites")])
    return InlineKeyboardMarkup(keyboard)
