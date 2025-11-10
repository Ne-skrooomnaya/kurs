import time
import hashlib
import hmac
import requests
import config

BYBIT_BASE_URL = "https://api.bybit.com"

def _generate_signature(secret, query_string):
    return hmac.new(secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

def _get_headers(api_key, api_secret, api_passphrase, params):
    timestamp = str(int(time.time() * 1000))
    # Для GET-запросов тело пустое, поэтому sign = timestamp + method + path + query
    recv_window = "5000"
    query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items())])
    val = f"{timestamp}GET/v5/market/tickers{query_string}{recv_window}"
    signature = _generate_signature(api_secret, val)

    return {
        "X-BAPI-SIGN-TYPE": "2",
        "X-BAPI-SIGN": signature,
        "X-BAPI-API-KEY": api_key,
        "X-BAPI-TIMESTAMP": timestamp,
        "X-BAPI-RECV-WINDOW": recv_window,
    }

def get_ticker_price(symbol: str):
    """Получает цену с Bybit через подписанный запрос (даже для публичных данных)"""
    try:
        params = {
            "category": "spot",
            "symbol": symbol
        }
        headers = _get_headers(
            config.BYBIT_API_KEY,
            config.BYBIT_SECRET_KEY,
            config.BYBIT_PASSPHRASE,
            params
        )
        url = f"{BYBIT_BASE_URL}/v5/market/tickers"
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()

        if data.get("retCode") == 0:
            return float(data["result"]["list"][0]["lastPrice"])
        else:
            print(f"Bybit API ошибка: {data.get('retMsg')}")
            return None
    except Exception as e:
        print(f"Исключение в get_ticker_price: {e}")
        return None

def get_usd_rate():
    # Bybit не имеет USDT/RUB → используем ЦБ РФ
    try:
        data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
        return data['Valute']['USD']['Value']
    except Exception as e:
        print(f"Ошибка ЦБ РФ (USD): {e}")
        return None

def get_eur_rate():
    try:
        data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
        return data['Valute']['EUR']['Value']
    except Exception as e:
        print(f"Ошибка ЦБ РФ (EUR): {e}")
        return None

def get_bitcoin_price():
    return get_ticker_price("BTCUSDT")