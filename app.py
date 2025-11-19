import requests
import json
from flask import Flask, request
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/webhook', methods=['POST'])
def webhook():
    data_raw = request.data.decode("utf-8")
    try:
        data = json.loads(data_raw)
    except Exception as e:
        return f"Invalid JSON: {e}", 400

    signal = data.get("signal", "")
    ticker  = data.get("ticker", "")
    close   = data.get("close", "")
    time    = data.get("time", "")

    message = f"{signal}  {ticker}\nSaat: {time}\nFiyat: {close}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    try:
        r = requests.post(url, json=payload)
        r.raise_for_status()
    except Exception as e:
        return f"Telegram send failed: {e}", 500

    return "OK", 200
