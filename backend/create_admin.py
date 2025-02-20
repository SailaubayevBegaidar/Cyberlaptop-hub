from pymongo import MongoClient
import bcrypt
from datetime import datetime, UTC

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['find_best_laptop']

# Данные администратора
admin_data = {
    'username': 'admin',
    'email': 'admin@example.com',
    'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
    'is_admin': True,
    'created_at': datetime.now(UTC)
}

# Проверка существования администратора
existing_admin = db.users.find_one({'username': 'admin'})
if not existing_admin:
    db.users.insert_one(admin_data)
    print("Администратор успешно создан!")
else:
    print("Администратор уже существует!") 