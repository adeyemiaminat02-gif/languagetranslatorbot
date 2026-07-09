import asyncio
from aiohttp import web
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from utils.config import BOT_TOKEN, PORT
from services.database import init_db
from utils.logger import logger

# Import handlers
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.about import about_handler
from handlers.history import history_handler
from handlers.favorites import favorites_handler, favorites_callback
from handlers.translate import (
    message_handler, process_translation_action, 
    language_page_callback, translation_execution_callback
)

async def handle_health_check(request):
    return web.Response(text="Bot running cleanly.", status=200)

async def main():
    # 1. Initialize DB Table Framework
    init_db()

    # 2. Build the Telegram Application instance
    application = Application.builder().token(BOT_TOKEN).build()

    # 3. Attach Handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("about", about_handler))
    application.add_handler(CommandHandler("history", history_handler))
    application.add_handler(CommandHandler("favorites", favorites_handler))
    
    application.add_handler(CallbackQueryHandler(process_translation_action, pattern="^action_translate$"))
    application.add_handler(CallbackQueryHandler(language_page_callback, pattern="^page_"))
    application.add_handler(CallbackQueryHandler(favorites_callback, pattern="^(managefav_|close_favorites)"))
    application.add_handler(CallbackQueryHandler(translation_execution_callback, pattern="^lang_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    # 4. Initialize and start Telegram Bot Engine
    await application.initialize()
    await application.start()
    
    # FIX: Removed the non-existent Application.DEFAULT_TYPE attribute assignment
    await application.updater.start_polling()
    logger.info("Telegram engine polling activated.")

    # 5. Start lightweight aiohttp server concurrently to satisfy Render HTTP health checks
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    logger.info(f"Health check web server running on port: {PORT}")

    # Keep loop alive continuously
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
