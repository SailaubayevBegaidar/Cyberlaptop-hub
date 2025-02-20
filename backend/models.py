from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = user_data['password']
        self.is_admin = user_data.get('is_admin', False)

class Laptop:
    def __init__(self, name, brand, price, specs):
        self.name = name
        self.brand = brand
        self.price = price
        self.specs = specs
        self.created_at = datetime.utcnow() 