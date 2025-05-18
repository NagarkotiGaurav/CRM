import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    MONGODB_SETTINGS = {
        'host': os.environ.get(
            'MONGODB_URI',
            'mongodb+srv://ankittarar703:qn2yV67wOuP6PV35@cluster0.jyuod1a.mongodb.net/customerdb?retryWrites=true&w=majority&tls=true'
        )
    }
    DEBUG = False
