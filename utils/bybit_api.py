import requests

def get_ticker_price(symbol: str):
    """
    Получает последнюю цену для пары на Bybit Spot.
    symbol: строка вида "BTCUSDT", "ETHUSDT" — без слеша!
    """
    try:
        url = "https://api.bybit.com/v5/market/tickers"
        params = {
            "category": "spot",
            "symbol": symbol
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Выбросит исключение, если HTTP-код не 200
        data = response.json()

        if data.get("retCode") == 0 and data.get("result"):
            price = float(data["result"]["list"][0]["lastPrice"])
            return price
        else:
            print(f"Ошибка Bybit API для {symbol}: {data.get('retMsg', 'Unknown')}")
            return None
    except Exception as e:
        print(f"Исключение при запросе {symbol}: {e}")
        return None


def get_usd_rate():
    """Получает курс USD/RUB через ЦБ РФ"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = response.json()
        return data['Valute']['USD']['Value']
    except Exception as e:
        print(f"Ошибка при получении курса USD через ЦБ: {e}")
        return None


def get_eur_rate():
    """Получает курс EUR/RUB через ЦБ РФ"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = response.json()
        return data['Valute']['EUR']['Value']
    except Exception as e:
        print(f"Ошибка при получении курса EUR через ЦБ: {e}")
        return None


def get_bitcoin_price():
    """Получает цену Биткоина в USD с Bybit"""
    return get_ticker_price("BTCUSDT")