import requests
import time
import config

_last_gold_price = None
_last_gold_update_time = 0
GOLD_CACHE_TTL = 900  # 15 минут

def get_gold_price_usd():
    """Возвращает цену золота в USD за унцию от GoldAPI (FOREXCOM)."""
    global _last_gold_price, _last_gold_update_time

    now = time.time()
    is_cache_expired = (now - _last_gold_update_time) >= GOLD_CACHE_TTL

    try:
        # Проверка 1: нужно ли обновлять кэш?
        if _last_gold_price is None or is_cache_expired:
            # Проверка 2: задан ли API-ключ?
            if not config.GOLD_API_KEY:
                print("❌ GOLD_API_KEY не задан в .env")
                return None

            # Проверка 3: формируем корректный URL (без пробелов!)
            url = "https://www.goldapi.io/api/XAU/USD"
            headers = {"x-access-token": config.GOLD_API_KEY}

            try:
                # Проверка 4: делаем запрос
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()  # Проверка HTTP-ошибок
            except requests.exceptions.Timeout:
                print("⚠️ GoldAPI: таймаут запроса")
                return None
            except requests.exceptions.ConnectionError:
                print("⚠️ GoldAPI: ошибка подключения")
                return None
            except requests.exceptions.HTTPError as e:
                print(f"⚠️ GoldAPI: HTTP ошибка {e.response.status_code}")
                return None
            except Exception as e:
                print(f"⚠️ GoldAPI: неизвестная ошибка запроса: {e}")
                return None

            try:
                # Проверка 5: парсим JSON
                data = response.json()
            except ValueError:
                print("❌ GoldAPI: ответ не в формате JSON")
                return None

            # Проверка 6: есть ли поле 'price'?
            if "price" in data:
                try:
                    raw_price = data["price"]
                    _last_gold_price = float(raw_price)
                    _last_gold_update_time = now
                    print(f"✅ ЗОЛОТО ОБНОВЛЕНО от GoldAPI: ${_last_gold_price:,.2f}/унция")
                    return _last_gold_price
                except (TypeError, ValueError):
                    print(f"❌ GoldAPI: 'price' не является числом: {data['price']}")
                    return None
            else:
                print(f"❌ GoldAPI: в ответе нет поля 'price'. Ответ: {data}")
                return None

        else:
            # Кэш ещё актуален
            print(f"🔁 ЗОЛОТО: используем кэш (${_last_gold_price:,.2f}/унция, обновление каждые 15 мин)")
            return _last_gold_price

    except Exception as e:
        print(f"⚠️ Неожиданная ошибка в get_gold_price_usd: {e}")
        return None