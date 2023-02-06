import os
from dotenv import load_dotenv

import logging
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram._update import Update

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I'm a bot that will process Twitter and FurAffinity URLs into neat Telegram messages. You just have to send a valid link to me.",
    )


if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
