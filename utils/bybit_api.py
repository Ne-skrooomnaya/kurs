import requests

BYBIT_BASE_URL = "https://api.bybit.com"

def get_ticker_price(symbol: str):
    try:
        params = {"category": "spot", "symbol": symbol}
        response = requests.get(f"{BYBIT_BASE_URL}/v5/market/tickers", params=params, timeout=10)
        data = response.json()
        if data.get("retCode") == 0 and data["result"]["list"]:
            return float(data["result"]["list"][0]["lastPrice"])
        else:
            print(f"Bybit: нет данных для {symbol}")
            return None
    except Exception as e:
        print(f"Bybit ошибка для {symbol}: {e}")
        return None

def get_bitcoin_price():
    return get_ticker_price("BTCUSDT")