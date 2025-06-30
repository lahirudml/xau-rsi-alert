import requests
import time

# --- YOUR CONFIG ---
TELEGRAM_TOKEN = 7977197268:AAHrBpxj_0Ps9RquxAYOe0Zkof655p9PC1k
TELEGRAM_CHAT_ID = 1468939509
TWELVE_DATA_API_KEY = c0b3c0f5fef848b0a5e8217f4b94ac5b
RSI_PERIOD = 5
UPPER = 80
LOWER = 20

last_rsi = None

def get_rsi():
    url = f"https://api.twelvedata.com/rsi?symbol=XAU/USD&interval=5min&time_period={RSI_PERIOD}&apikey={TWELVE_DATA_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data['values'][0]['rsi'])
    except Exception as e:
        print("Error:", e)
        return None

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': msg}
    requests.post(url, data=data)

while True:
    try:
        rsi = get_rsi()
        print("RSI:", rsi)
        if rsi is not None and last_rsi is not None:
            if last_rsi <= UPPER and rsi > UPPER:
                send_telegram(f"📈 RSI crossed above 80: {rsi:.2f}")
            elif last_rsi >= UPPER and rsi < UPPER:
                send_telegram(f"📉 RSI crossed below 80: {rsi:.2f}")
            elif last_rsi <= LOWER and rsi > LOWER:
                send_telegram(f"📈 RSI crossed above 20: {rsi:.2f}")
            elif last_rsi >= LOWER and rsi < LOWER:
                send_telegram(f"📉 RSI crossed below 20: {rsi:.2f}")
        last_rsi = rsi
    except Exception as e:
        print("Main Loop Error:", e)
    time.sleep(300)  # Wait 5 minutes

