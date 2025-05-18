from flask import Flask, jsonify, render_template, request, redirect
#from mongoengine import disconnect
from pymongo import MongoClient
from model import init_db
from bson.objectid import ObjectId

init_db()

from model import   db,Customers_collection,Inventory_collection

#print(f"db is {db.list_collections}")
#print("Collections:", list(db.list_collection_names()))

# print(f"customer colection {Customers_collection}")
app = Flask(__name__)


@app.route('/')
def home():
    for document in Customers_collection.find({}):
        print(document)
    
    return "Hello, Flask!"

@app.route("/customer")
def customer_page():
    customer = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "address": "123 Main Street, City"
    }
    return render_template("customer.html", customer=customer)

@app.route("/inventory")
def inventory_page():
    package = {
        "id": 1,
        "email": "john@example.com",
        "phone": "123-456-7890",
        "address": "123 Main Street, City"
    }
    return render_template("inventory.html", package=package)

# ---- Customer Routes ----

@app.route('/create-customer', methods=['POST'])
def create_customer():
    try:
        new_customer = {
            "name": request.form['name'],
        "address": request.form['address'],
        "email": request.form['email'],
        "phone_number": request.form['phone_number'],
        "number_of_packages": int(request.form.get('number_of_packages', 0)),
        "returned_number": int(request.form.get('returned_number', 0)),
        "packages": []
        }
        Customers_collection.insert_one(new_customer)
        return redirect('/')  # Redirect to homepage or customer list after success
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customers', methods=['GET'])
def get_all_customers():
    customers = Customers_collection.find({})
    result = []
    for c in customers:
        result.append({
            "id": str(c['_id']),
            "name": c['name'],
            "address": c['address'],
            "email": c['email'],
            "phone_number": c['phone_number'],
            "number_of_packages": c['number_of_packages'],
            "returned_number": c['returned_number']
        })
        
    return jsonify(result)

@app.route('/customers/<string:id>', methods=['GET'])
def get_customer(id):
    try:
        customer = Customers_collection.find_one({"_id": ObjectId(id)})
        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({
            "id": str(customer["_id"]),
            "name": customer.get("name"),
            "address": customer.get("address"),
            "email": customer.get("email"),
            "phone_number": customer.get("phone_number"),
            "number_of_packages": customer.get("number_of_packages"),
            "returned_number": customer.get("returned_number")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customers/<string:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    
    try:
        update_result = Customers_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": data.get("name"),
                "address": data.get("address"),
                "email": data.get("email"),
                "phone_number": data.get("phone_number"),
                "number_of_packages": data.get("number_of_packages"),
                "returned_number": data.get("returned_number")
            }}
        )
        if update_result.matched_count == 0:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify({"message": "Customer updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/customers/<string:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        # Convert string id to ObjectId
        object_id = ObjectId(id)
    except Exception:
        return jsonify({"error": "Invalid customer ID"}), 400
    
    result = Customers_collection.delete_one({"_id": object_id})

    if result.deleted_count == 1:
        return jsonify({"message": "Customer deleted successfully"}), 200
    else:
        return jsonify({"error": "Customer not found"}), 404
# ---- Package Routes ----

def serialize_item(item):
    item['_id'] = str(item['_id'])
    return item

@app.route('/items', methods=['GET'])
def get_items():
    items = list(Inventory_collection.find())
    return jsonify([serialize_item(item) for item in items]), 200

# POST: Add new item
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = {
        'name': data['name'],
        'quantity': int(data['quantity']),
        'price': float(data['price'])
    }
    result = Inventory_collection.insert_one(item)
    item['_id'] = str(result.inserted_id)
    return jsonify(item), 201

# PUT: Update item by ID
@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    updated_data = {
        'name': data['name'],
        'quantity': int(data['quantity']),
        'price': float(data['price'])
    }
    result = Inventory_collection.update_one({'_id': ObjectId(item_id)}, {'$set': updated_data})
    if result.matched_count:
        return jsonify({'_id': item_id, **updated_data}), 200
    return jsonify({'error': 'Item not found'}), 404

# DELETE: Delete item by ID
@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    result = Inventory_collection.delete_one({'_id': ObjectId(item_id)})
    if result.deleted_count:
        return jsonify({'message': 'Item deleted'}), 200
    return jsonify({'error': 'Item not found'}), 404


@app.route('/packages/<string:customer_id>', methods=['POST'])
def create_package(customer_id):
    data = request.json
    try:
        customer = Customer.objects.get_or_404(id=customer_id)
        package = Package(
            name=data['name'],
            cod=data.get('cod', False),
            address=data['address'],
            phone=data['phone'],
            email=data['email'],
            quant=data.get('quant', 1)
        )
        customer.packages.append(package)
        customer.number_of_packages += 1
        customer.save()
        return jsonify({'message': 'Package added to customer'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/packages/<string:customer_id>', methods=['GET'])
def get_packages(customer_id):
    customer = Customer.objects.get_or_404(id=customer_id)
    packages = []
    for p in customer.packages:
        packages.append({
            "name": p.name,
            "cod": p.cod,
            "address": p.address,
            "phone": p.phone,
            "email": p.email,
            "quant": p.quant
        })
    return jsonify(packages)

@app.route('/packages/<string:customer_id>/<int:package_index>', methods=['DELETE'])
def delete_package(customer_id, package_index):
    customer = Customer.objects.get_or_404(id=customer_id)
    try:
        del customer.packages[package_index]
        customer.number_of_packages -= 1
        customer.save()
        return jsonify({'message': 'Package removed'})
    except IndexError:
        return jsonify({'error': 'Package index out of range'}), 400


if __name__ == '__main__':
    app.run(debug=True)
