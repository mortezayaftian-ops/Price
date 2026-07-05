import os
import json
from telegram import Bot
from datetime import datetime

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = -1004297055826

bot = Bot(TOKEN)

DATA_FILE = "prices.json"

def load_prices():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def main():
    prices = load_prices()

    if not prices:
        return

    values = [p["price"] for p in prices]

    high = max(values)
    low = min(values)
    last = values[-1]

    text = f"""📊 گزارش روزانه دلار

📈 سقف: {high:,}
📉 کف: {low:,}
💵 آخرین: {last:,}

#REPORT"""

    bot.send_message(chat_id=CHANNEL_ID, text=text)

if __name__ == "__main__":
    main()
