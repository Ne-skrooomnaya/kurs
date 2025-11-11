import requests

BYBIT_URL = "https://api.bybit.com/v5/market/tickers"

def get_bitcoin_price():
    try:
        params = {"category": "spot", "symbol": "BTCUSDT"}
        response = requests.get(BYBIT_URL, params=params, timeout=15)
        data = response.json()
        if data.get("retCode") == 0 and data["result"]["list"]:
            price = float(data["result"]["list"][0]["lastPrice"])
            print(f"✅ BTC: ${price:,.0f}")
            return price
        else:
            print("❌ Bybit: нет данных для BTCUSDT")
            return None
    except Exception as e:
        print(f"❌ Bybit ошибка: {e}")
        return None