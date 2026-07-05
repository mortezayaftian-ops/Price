import re
from telegram import Bot

TOKEN = "PUT_IN_SECRETS"
CHANNEL_ID = -1004297055826

bot = Bot(TOKEN)

def extract_price(text):
    match = re.search(r'(\d{2,3}(?:,\d{3})+)', text)
    return match.group(1) if match else None

def main():
    updates = bot.get_updates(limit=20)

    last_text = None
    for u in reversed(updates):
        if u.channel_post:
            last_text = u.channel_post.text
            break

    if not last_text:
        return

    if "نقدی" in last_text:
        kind = "نقدی"
    elif "فردایی" in last_text:
        kind = "فردایی"
    else:
        return

    price = extract_price(last_text)

    bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"💵 دلار\n\n💰 {kind}\n💲 {price}\n\n#DOLLAR"
    )

if __name__ == "__main__":
    main()
