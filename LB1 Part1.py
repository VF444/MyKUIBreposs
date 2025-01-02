import requests

from datetime import datetime, timedelta

# Отримуємо дати попереднього тижня

base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json"

dates = [(datetime.now() - timedelta(days=i)).strftime('%Y%m%d') for i in range(1, 8)]

# Отримуємо дані для кожного дня

rates = {}

for date in dates:

    try:

        response = requests.get(base_url.format(date=date))

        response.raise_for_status()  # Перевірка статусу запиту

        data = response.json()

        if data:  # Перевірка, чи дані не порожні

            rates[date] = data

        else:

            print(f"Пустий результат для {date}")

    except requests.exceptions.RequestException as e:

        print(f"Помилка під час отримання даних для {date}: {e}")

    # Виводимо отримані курси валют

for date, data in rates.items():

    print(f"Дата: {date}")

    for currency in data:
        print(f"  Валюта: {currency['cc']}, Курс: {currency['rate']}") 