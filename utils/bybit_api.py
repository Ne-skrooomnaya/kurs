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
            "symbol": symbol  # Важно: без слеша!
        }
        response = requests.get(url, params=params, timeout=10)
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
    """Получает курс USDT к USD через BTC/USDT и BTC/USD (если USDT/RUB недоступен)"""
    # На Bybit нет USDT/RUB, поэтому используем косвенный метод или просто показываем USD как 1
    # Для простоты: если мы не можем получить RUB, покажем USD как 1 (или используем другой источник)
    # Но так как вы хотите RUB — давайте попробуем найти USDT/RUB через другой способ

    # Попробуем получить USDT/RUB через другую биржу или вернём None
    # Альтернатива: использовать CBR API для USD/RUB
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        data = response.json()
        return data['Valute']['USD']['Value']
    except Exception as e:
        print(f"Ошибка при получении курса USD через ЦБ: {e}")
        return None


def get_eur_rate():
    """Получает курс EUR к рублю через ЦБ РФ"""
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