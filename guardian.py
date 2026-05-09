import yfinance as yf
import requests
import time
import os

TOKEN = "8457858315:AAGPSHq0UsfPv8MZ733tHs40gAOxwvx7G0o"
CHAT_ID = "5916986433"

def send_alert(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}, timeout=10)
    except: pass

def monitor():
    send_alert("🛡️ <b>Guardian Aktif:</b> Penjaga modal Kapten sudah berpatroli!")
    while True:
        try:
            if not os.path.exists("portfolio.txt"):
                open("portfolio.txt", "w").close()
            
            with open("portfolio.txt", "r") as f:
                stocks = list(set([line.strip() for line in f.readlines() if line.strip()]))
            
            for s in stocks:
                ticker = yf.Ticker(f"{s}.JK")
                df = ticker.history(period="2d")
                if df.empty: continue
                
                now = df['Close'].iloc[-1]
                prev = df['Close'].iloc[-2]
                change = ((now - prev) / prev) * 100
                
                # Logika Trailing Stop: $ \Delta \% \le -5\% $
                if change <= -5.0:
                    send_alert(f"🚨 <b>EXIT SIGNAL: {s}</b>\nTurun {change:.2f}%!\nSegera amankan modal.")
            
            time.sleep(900) # Cek setiap 15 menit
        except Exception as e:
            time.sleep(60)

if __name__ == "__main__":
    monitor()