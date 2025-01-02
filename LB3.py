from flask import Flask, jsonify, request, abort
from flask_httpauth import HTTPBasicAuth

# Ініціалізація Flask-додатка
app = Flask(__name__)
auth = HTTPBasicAuth()

# Дані для Basic Authentication
users = {
    "admin": "password123",
    "user": "mypassword"
}

# Дані каталогу товарів (зберігаються в словнику)
catalog = {
    1: {"name": "Coffee Arabica", "price": 100.25, "weight": 250},
    2: {"name": "Coffee Robusta", "price": 80.50, "weight": 300}
}

# Аутентифікація
@auth.get_password
def get_password(username):
    return users.get(username)

@auth.error_handler
def unauthorized():
    return jsonify({"error": "Unauthorized access"}), 401

# Ендпоінт для роботи з усім каталогом
@app.route('/items', methods=['GET', 'POST'])
@auth.login_required
def manage_items():
    if request.method == 'GET':
        return jsonify(catalog)

    elif request.method == 'POST':
        if not request.json or not all(k in request.json for k in ["name", "price", "weight"]):
            abort(400, description="Invalid input. JSON with 'name', 'price', and 'weight' required.")
        new_id = max(catalog.keys()) + 1 if catalog else 1
        catalog[new_id] = {
            "name": request.json["name"],
            "price": request.json["price"],
            "weight": request.json["weight"]
        }
        return jsonify({"id": new_id, "message": "Item added successfully."}), 201

# Ендпоінт для роботи з конкретним товаром
@app.route('/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def manage_item(item_id):
    if item_id not in catalog:
        abort(404, description="Item not found.")

    if request.method == 'GET':
        return jsonify(catalog[item_id])

    elif request.method == 'PUT':
        if not request.json:
            abort(400, description="Invalid input. JSON required.")
        item = catalog[item_id]
        item.update({
            "name": request.json.get("name", item["name"]),
            "price": request.json.get("price", item["price"]),
            "weight": request.json.get("weight", item["weight"])
        })
        return jsonify({"message": "Item updated successfully."})

    elif request.method == 'DELETE':
        del catalog[item_id]
        return jsonify({"message": "Item deleted successfully."})

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
