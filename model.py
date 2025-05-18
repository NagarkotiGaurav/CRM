from flask import Flask
#from flask_mongoengine import MongoEngine
from pymongo import MongoClient
app = Flask(__name__)

client=None
db=None
Customers_collection=None
Inventory_collection = None
# MongoDB Atlas configuration
def init_db():
    MONGO_URI='mongodb+srv://ankittarar703:qn2yV67wOuP6PV8v@cluster0.jyuod1a.mongodb.net/customerdb?retryWrites=true&w=majority&appName=Cluster0'
    global client,db,Customers_collection,Inventory_collection
    try:
        client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
        db = client.get_database()
            # Test the connection
        db = client['customerdb']
        Customers_collection = db['customers']
        Inventory_collection=db['inventory']
        print(db,"succesful")
    except Exception as e :
        print(f"error in connecting :{e}")    

