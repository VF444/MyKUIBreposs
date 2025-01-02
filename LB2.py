# Імпортуємо необхідні бібліотеки
from flask import Flask, request, jsonify, Response
import requests
import xml.etree.ElementTree as ET

# Створюємо додаток Flask
app = Flask(__name__)


# Крок 2: Простий обробник GET-запиту, що повертає "Hello World!"
@app.route('/')
def hello_world():
    return "Hello World!"


# Крок 3: Обробка GET-запиту зі шляхом і параметрами
@app.route('/currency')
def currency_static():
    # Отримуємо параметр key із запиту
    key = request.args.get('key')
    if key:
        return "USD - 41.5"
    return "Missing key parameter."


# Крок 4: Обробка заголовків запиту
@app.route('/content-type')
def content_type_handler():
    # Зчитуємо заголовок Content-Type
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Повертаємо JSON-відповідь
        return jsonify(message="This is JSON content")
    elif content_type == 'application/xml':
        # Формуємо XML-відповідь
        root = ET.Element("response")
        child = ET.SubElement(root, "message")
        child.text = "This is XML content"
        return Response(ET.tostring(root), mimetype='application/xml')
    else:
        # Повертаємо текстову відповідь за замовчуванням
        return "This is plain text content"


# Крок 5: Динамічне отримання курсу валют з API НБУ
@app.route('/currency/dynamic')
def currency_dynamic():
    # Отримуємо параметр param із запиту
    param = request.args.get('param')
    nbu_api = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={}&json"

    if param == 'today':
        # Отримуємо поточну дату
        date = requests.get("https://worldtimeapi.org/api/timezone/Europe/Kiev").json()['datetime'][:10]
    elif param == 'yesterday':
        # Обчислюємо дату вчорашнього дня
        from datetime import datetime, timedelta
        date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    else:
        # Якщо параметр некоректний, повертаємо повідомлення про помилку
        return "Invalid parameter. Use 'today' or 'yesterday'."

    # Надсилаємо запит до API НБУ
    response = requests.get(nbu_api.format(date))
    if response.status_code == 200:
        data = response.json()
        if data:
            # Повертаємо курс USD на зазначену дату
            return f"USD rate on {date}: {data[0]['rate']}"
    # У разі помилки повертаємо повідомлення про це
    return "Could not fetch currency rate."


# Запускаємо сервер на порту 8000
if __name__ == '__main__':
    app.run(port=8000)
