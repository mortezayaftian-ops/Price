import os
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = -1004297055826

bot = Bot(TOKEN)

bot.send_message(
    chat_id=CHANNEL_ID,
    text="✅ ربات با موفقیت اجرا شد."
)
