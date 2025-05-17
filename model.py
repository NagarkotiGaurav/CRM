from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

# MongoDB Atlas configuration
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://ankittarar703:qn2yV67wOuP6PV35@cluster0.jyuod1a.mongodb.net/customerdb?retryWrites=true&w=majority'
}

db = MongoEngine(app)

# Define Package as an embedded document
class Package(db.EmbeddedDocument):
    name = db.StringField(required=True)
    cod = db.BooleanField(default=False)
    address = db.StringField(required=True)
    phone = db.StringField(required=True)
    email = db.StringField(required=True)
    quant = db.IntField()

# Define Customer as a document with embedded packages
class Customer(db.Document):
    name = db.StringField(required=True, max_length=100)
    address = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    phone_number = db.StringField(required=True)
    number_of_packages = db.IntField(default=0)
    returned_number = db.IntField(default=0)

    packages = db.EmbeddedDocumentListField(Package)

    def __str__(self):
        return f'<Customer {self.name}>'

# Run the app (for testing only)
if __name__ == '__main__':
    app.run(debug=True)
