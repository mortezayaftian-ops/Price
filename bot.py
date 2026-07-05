import os
import re
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = -1004297055826

bot = Bot(TOKEN)

def extract_price(text):
    match = re.search(r'(\d{2,3}(?:,\d{3})+)', text)
    return match.group(1) if match else None

def main():
    updates = bot.get_updates(limit=30)

    last = None
    for u in reversed(updates):
        if u.channel_post and u.channel_post.text:
            last = u.channel_post.text
            break

    if not last:
        return

    kind = None
    if "نقدی" in last:
        kind = "نقدی"
    elif "فردایی" in last:
        kind = "فردایی"
    else:
        return

    price = extract_price(last)

    if not price:
        return

    text = f"""💵 دلار تهران

💰 نوع: {kind}
💲 قیمت: {price}

#DOLLAR"""

    bot.send_message(chat_id=CHANNEL_ID, text=text)

if __name__ == "__main__":
    main()
