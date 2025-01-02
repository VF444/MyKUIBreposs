import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Отримуємо дати попереднього тижня
base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json"
dates = [(datetime.now() - timedelta(days=i)).strftime('%Y%m%d') for i in range(1, 8)]

# Вибір валют для аналізу: Фунт, Долар та Євро
currencies_to_track = ["USD", "EUR", "GBP"]

# Отримуємо дані для кожного дня
rates = {currency: [] for currency in currencies_to_track}
dates_with_data = []  # Зберігаємо дати, для яких вдалося отримати дані

for date in dates:
    try:
        response = requests.get(base_url.format(date=date))
        response.raise_for_status()  # Перевірка статусу запиту
        data = response.json()

        # Додаємо курси для кожної валюти
        daily_rates = {item["cc"]: item["rate"] for item in data if item["cc"] in currencies_to_track}
        if daily_rates:  # Якщо для дати є дані
            dates_with_data.append(date)
            for currency in currencies_to_track:
                rates[currency].append(daily_rates.get(currency, None))  # None, якщо даних немає
    except requests.exceptions.RequestException as e:
        print(f"Помилка під час отримання даних для {date}: {e}")

# Побудова графіка
plt.figure(figsize=(12, 6))
for currency, rate_values in rates.items():
    if any(rate_values):  # Тільки якщо є дані для валюти
        plt.plot(dates_with_data, rate_values, marker='o', label=currency)

# Налаштування графіка
plt.title("Курси світових валют за останній тиждень (НБУ)")
plt.xlabel("Дата")
plt.ylabel("Курс (грн)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Відображення графіка
plt.show()


