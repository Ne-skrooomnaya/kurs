import requests

def get_ticker_price(symbol: str):
    """
    Получает цену пары с Bybit Spot (публичный API, без ключей)
    Пример: symbol = "BTCUSDT"
    """
    try:
        url = "https://api.bybit.com/v5/market/tickers"
        params = {"category": "spot", "symbol": symbol}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("retCode") == 0:
                return float(data["result"]["list"][0]["lastPrice"])
        print(f"Bybit: ошибка для {symbol}, статус {response.status_code}")
        return None
    except Exception as e:
        print(f"Исключение при запросе {symbol}: {e}")
        return None

def get_usd_rate():
    # Bybit не имеет USDT/RUB → используем ЦБ РФ
    try:
        data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
        return data['Valute']['USD']['Value']
    except:
        return None

def get_eur_rate():
    # Bybit не имеет EUR/RUB → используем ЦБ РФ
    try:
        data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
        return data['Valute']['EUR']['Value']
    except:
        return None

def get_bitcoin_price():
    return get_ticker_price("BTCUSDT")