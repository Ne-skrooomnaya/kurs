import requests
import time
import config
from utils.fiat_api import get_usd_rate, _get_gold_price_rub_per_gram_from_cbr

_last_price = None
_last_time = 0
TTL = 900  # 15 минут

def get_gold_price_usd():
    global _last_price, _last_time
    now = time.time()

    if _last_price is not None and (now - _last_time) < TTL:
        print(f"🔁 ЗОЛОТО: кэш (${_last_price:,.2f}/унция)")
        return _last_price

    # === ОСНОВНОЙ ИСТОЧНИК: FMP ===
    if config.FMP_API_KEY:
        try:
            url = "https://financialmodelingprep.com/stable/quote"  # ← исправлено: без пробелов!
            params = {"symbol": "GCUSD", "apikey": config.FMP_API_KEY}
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            if data and "price" in data[0]:
                price = float(data[0]["price"])
                _last_price = price
                _last_time = now
                print(f"✅ ЗОЛОТО (FMP): ${price:,.2f}/унция")
                return price
        except Exception as e:
            print(f"⚠️ FMP ошибка: {e}")

    # === РЕЗЕРВНЫЙ ИСТОЧНИК: ЦБ РФ ===
    print("⚠️ Используем резервный источник для золота: ЦБ РФ")
    gold_rub_per_gram = _get_gold_price_rub_per_gram_from_cbr()
    if gold_rub_per_gram is None:
        print("❌ Не удалось получить золото даже из ЦБ РФ")
        return None

    usd_rub = get_usd_rate()
    if usd_rub is None:
        print("❌ Не удалось получить USD/RUB для пересчёта золота")
        return None

    grams_per_ounce = 31.1035
    gold_rub_per_ounce = gold_rub_per_gram * grams_per_ounce
    gold_usd = gold_rub_per_ounce / usd_rub

    _last_price = gold_usd
    _last_time = now
    print(f"✅ ЗОЛОТО (резерв, ЦБ РФ): ${gold_usd:,.2f}/унция")
    return gold_usd