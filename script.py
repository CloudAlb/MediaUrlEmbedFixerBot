import os
from dotenv import load_dotenv

from enum import Enum

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


class ValidUrls(Enum):
    TWITTER = "twitter.com"
    FURAFFINITY = "furaffinity.net"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello! I'm a bot that will process Twitter and FurAffinity URLs into neat Telegram messages. You just have to send a valid link to me.",
    )


def is_valid_url(url):
    valid_url_match = ""

    if not url.startswith("https://"):
        return

    for valid_url in ValidUrls:
        if valid_url.value in url.lower():
            valid_url_match = valid_url
            break

    return valid_url_match


async def process_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    valid_url_match = is_valid_url(update.message.text)

    if not valid_url_match:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="URL is invalid."
        )
        return

    formatted_url = url.split("?")[0]

    match valid_url_match:
        case ValidUrls.TWITTER:
            formatted_url = formatted_url.replace(
                ValidUrls.TWITTER.value, "fx" + ValidUrls.TWITTER.value
            )
        case ValidUrls.FURAFFINITY:
            formatted_url = formatted_url.replace(
                ValidUrls.FURAFFINITY.value, "fx" + ValidUrls.FURAFFINITY.value
            )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_url)


if __name__ == "__main__":
    load_dotenv()
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    process_url_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), process_url)

    application.add_handler(start_handler)
    application.add_handler(process_url_handler)

    application.run_polling()
