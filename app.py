from flask import Flask, request
import requests
from datetime import datetime
import os
import pytz

app = Flask(__name__)

# Telegram bilgileri
BOT_TOKEN = "8512959734:AAEtC6AbLHY-S0tdNohiAODl_Udoq5794us"
CHAT_ID = "-5017329899"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    signal = data.get("signal")
    ticker = data.get("ticker")
    price = data.get("close")
    time_raw = data.get("time")

    # UTC → Türkiye saati
    try:
        dt = datetime.fromisoformat(time_raw.replace("Z", "+00:00"))
        istanbul_tz = pytz.timezone("Europe/Istanbul")
        dt_tr = dt.astimezone(istanbul_tz)
        date_str = dt_tr.strftime("%Y-%m-%d")
        time_str = dt_tr.strftime("%H:%M:%S")
    except:
        date_str = time_raw
        time_str = ""

    message = f"{signal}   {ticker}\nSaat:  {date_str}     {time_str}\nFiyat:  {price}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

    return {"status": "ok"}

@app.route("/")
def home():
    return "Bot çalışıyor!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
