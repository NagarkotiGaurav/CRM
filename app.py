from flask import Flask, jsonify, render_template, request
from model import Customer, Package, db

app = Flask(__name__)

# Connect to MongoDB Atlas
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://ankittarar703:qn2yV67wOuP6PV35@cluster0.jyuod1a.mongodb.net/your_db_name?retryWrites=true&w=majority'
}

db.init_app(app)

@app.route('/')
def home():
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

@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    try:
        new_customer = Customer(
            name=data['name'],
            address=data['address'],
            email=data['email'],
            phone_number=data['phone_number'],
            number_of_packages=data.get('number_of_packages', 0),
            returned_number=data.get('returned_number', 0),
            packages=[]
        )
        new_customer.save()
        return jsonify({"message": "Customer created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/customers', methods=['GET'])
def get_all_customers():
    customers = Customer.objects()
    result = []
    for c in customers:
        result.append({
            "id": str(c.id),
            "name": c.name,
            "address": c.address,
            "email": c.email,
            "phone_number": c.phone_number,
            "number_of_packages": c.number_of_packages,
            "returned_number": c.returned_number
        })
    return jsonify(result)

@app.route('/customers/<string:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.objects.get_or_404(id=id)
    return jsonify({
        "id": str(customer.id),
        "name": customer.name,
        "address": customer.address,
        "email": customer.email,
        "phone_number": customer.phone_number,
        "number_of_packages": customer.number_of_packages,
        "returned_number": customer.returned_number
    })

@app.route('/customers/<string:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.objects.get_or_404(id=id)
    data = request.json

    customer.update(
        name=data.get('name', customer.name),
        address=data.get('address', customer.address),
        email=data.get('email', customer.email),
        phone_number=data.get('phone_number', customer.phone_number),
        number_of_packages=data.get('number_of_packages', customer.number_of_packages),
        returned_number=data.get('returned_number', customer.returned_number)
    )
    return jsonify({"message": "Customer updated successfully"})

@app.route('/customers/<string:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.objects.get_or_404(id=id)
    customer.delete()
    return jsonify({"message": "Customer deleted successfully"})

# ---- Package Routes ----

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
