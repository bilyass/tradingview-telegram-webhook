from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# Ortam değişkenleri
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID       = os.getenv("CHAT_ID")

# Ana sayfa kontrol
@app.route('/')
def home():
    return "Bot Çalışıyor"

# Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Eğer JSON string olarak geldiyse dict'e çevir
    if isinstance(data, str):
        data = json.loads(data)

    signal = data.get("signal", "")
    ticker  = data.get("ticker", "")
    close   = data.get("close", "")
    time    = data.get("time", "")

    message = f"{signal}  {ticker}\nSaat: {time}\nFiyat: {close}"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    requests.post(url, json=payload)

    return "OK", 200

# Test route
@app.route('/test')
def test():
    message = "Webhook test mesajı başarılı."
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)
    return "Test OK", 200
