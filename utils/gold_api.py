# utils/gold_api.py

import requests
import time
import config

_last_price = None
_last_time = 0
TTL = 900  # 15 минут

def get_gold_price_usd():
    global _last_price, _last_time
    now = time.time()

    if _last_price is not None and (now - _last_time) < TTL:
        print(f"🔁 ЗОЛОТО: кэш (${_last_price:,.2f}/унция)")
        return _last_price

    if not config.FMP_API_KEY:
        print("❌ FMP_API_KEY не задан в .env")
        return None

    try:
        url = "https://financialmodelingprep.com/stable/quote"
        params = {"symbol": "GCUSD", "apikey": config.FMP_API_KEY}
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not data or "price" not in data[0]:
            print(f"❌ FMP: неожиданный формат ответа: {data}")
            return None

        price = float(data[0]["price"])
        _last_price = price
        _last_time = now
        print(f"✅ ЗОЛОТО (FMP): ${price:,.2f}/унция")
        return price

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("❌ FMP: неверный API-ключ")
        elif response.status_code == 403:
            print("❌ FMP: доступ запрещён (проверьте эндпоинт и символ)")
        elif response.status_code == 429:
            print("❌ FMP: превышен лимит запросов (250/день)")
        else:
            print(f"❌ FMP HTTP ошибка {response.status_code}: {e}")
        return None
    except Exception as e:
        print(f"❌ FMP ошибка: {e}")
        return None