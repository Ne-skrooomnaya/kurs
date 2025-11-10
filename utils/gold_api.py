import requests
from datetime import date
from bs4 import BeautifulSoup

def get_gold_price():
    """Получает учетную цену золота от ЦБ РФ в рублях за грамм."""
    try:
        today = date.today()
        url = f"https://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.From=01.07.2008&UniDbQuery.To=21.10.2025&UniDbQuery.Gold=true&UniDbQuery.so=1"

        response = requests.get(url)
        response.raise_for_status()
        text = response.text

        soup = BeautifulSoup(text, 'html.parser')

        # Попытка найти таблицу с классом "data"
        table = soup.find('table', class_='data')
        if not table:
            print("Не найдена таблица с классом 'data' на сайте ЦБ.")
            return None

        # Получаем все строки таблицы
        rows = table.find_all('tr')
        if not rows or len(rows) < 2:
            print("В таблице на сайте ЦБ нет данных о золоте.")
            return None

        # Берем последнюю строку (самая свежая дата)
        last_row = rows[-1]
        # Ищем все ячейки (td) в строке
        cells = last_row.find_all('td')

       # Проверяем, есть ли ячейки в строке
        if not cells or len(cells) < 2:
            print("В строке данных о золоте на сайте ЦБ недостаточно ячеек.")
            return None

        # Пытаемся найти ячейку, содержащую цену (ищем текст, похожий на число)
        price_cell = None
        for cell in cells:
            text = cell.text.replace(',', '.').strip()
            try:
                float(text)  # Пытаемся преобразовать в число
                price_cell = cell
                break  # Нашли ячейку с ценой
            except ValueError:
                pass  # Это не число

        if not price_cell:
            print("Не удалось найти ячейку с ценой золота на сайте ЦБ.")
            return None

        # Извлекаем цену из найденной ячейки
        price_str = price_cell.text.replace(',', '.').strip()
        try:
            price = float(price_str)
            return price
        except ValueError:
            print("Не удалось преобразовать цену золота в число на сайте ЦБ.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к сайту ЦБ: {e}")
        return None
    except Exception as e:
        print(f"Общая ошибка при получении цены золота от ЦБ: {e}")
        return None