import os
import re
import json
from telegram import Bot

TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = -1004297055826

bot = Bot(TOKEN)

STATE_FILE = "state.json"
PRICES_FILE = "prices.json"

# ---------- load/save ----------
def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"last_price": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def load_prices():
    try:
        with open(PRICES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_prices(prices):
    with open(PRICES_FILE, "w") as f:
        json.dump(prices, f)

# ---------- price ----------
def extract_price(text):
    if not text:
        return None
    match = re.search(r'(\d{2,3}(?:,\d{3})+)', text)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))

def save_price(price):
    prices = load_prices()
    prices.append(price)
    prices = prices[-50:]  # فقط 50 تای آخر
    save_prices(prices)

# ---------- main ----------
def main():
    state = load_state()

    try:
        updates = bot.get_updates(limit=10, timeout=20)
    except:
        return

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

    # ❌ جلوگیری از تکرار
    if state["last_price"] == price:
        return

    # 📊 تغییر قیمت
    change_text = ""
    if state["last_price"]:
        diff = price - state["last_price"]
        if diff > 0:
            change_text = f"🟢 +{diff:,}"
        elif diff < 0:
            change_text = f"🔴 {diff:,}"
        else:
            change_text = "⚪ بدون تغییر"

    text = f"""💵 دلار تهران

💰 نوع: {kind}
💲 قیمت: {price:,}

{change_text}

#DOLLAR"""
