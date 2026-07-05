import os
import re
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = -1004297055826

bot = Bot(TOKEN)

def extract_price(text):
    if not text:
        return None
    match = re.search(r'(\d{2,3}(?:,\d{3})+)', text)
    return match.group(1) if match else None

def main():
    try:
        updates = bot.get_updates(limit=10, timeout=20)
    except Exception as e:
        print("Error:", e)
        return

    last = None
    for u in reversed(updates):
        if u.channel_post and u.channel_post.text:
            last = u.channel_post.text
            break

    if not last:
        return

    if "نقدی" in last:
        kind = "نقدی"
    elif "فردایی" in last:
        kind = "فردایی"
    else:
        return

    price = extract_price(last)

    if not price:
        return

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"""💵 دلار تهران

💰 نوع: {kind}
💲 قیمت: {price}

#DOLLAR"""
    )

if __name__ == "__main__":
    main()
