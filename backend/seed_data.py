from pymongo import MongoClient
from datetime import datetime, UTC
import bcrypt

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['find_best_laptop']

# Очистка существующих данных
db.laptops.delete_many({})
db.users.delete_many({})
db.reviews.delete_many({})

# 1. Данные для пользователей
users = [
    {
        "username": "john_doe",
        "password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()),
        "email": "john@example.com",
        "created_at": datetime.now(UTC)
    },
    {
        "username": "alice_smith",
        "password": bcrypt.hashpw("password456".encode('utf-8'), bcrypt.gensalt()),
        "email": "alice@example.com",
        "created_at": datetime.now(UTC)
    }
]

# 2. Данные для ноутбуков
laptops = [
    {
        "name": "MacBook Pro 16",
        "brand": "Apple",
        "price": 2399,
        "specs": {
            "processor": "M1 Pro",
            "ram": "16GB",
            "storage": "512GB SSD",
            "display": "16-inch Retina",
            "gpu": "16-core GPU"
        },
        "in_stock": True,
        "created_at": datetime.now(UTC)
    },
    {
        "name": "Dell XPS 15",
        "brand": "Dell",
        "price": 1799,
        "specs": {
            "processor": "Intel i7-11800H",
            "ram": "32GB",
            "storage": "1TB SSD",
            "display": "15.6-inch 4K",
            "gpu": "NVIDIA RTX 3050 Ti"
        },
        "in_stock": True,
        "created_at": datetime.now(UTC)
    },
    {
        "name": "ThinkPad X1 Carbon",
        "brand": "Lenovo",
        "price": 1599,
        "specs": {
            "processor": "Intel i7-1165G7",
            "ram": "16GB",
            "storage": "512GB SSD",
            "display": "14-inch 4K",
            "gpu": "Intel Iris Xe"
        },
        "in_stock": False,
        "created_at": datetime.now(UTC)
    }
]

# 3. Данные для отзывов
reviews = [
    {
        "laptop_name": "MacBook Pro 16",
        "user_username": "john_doe",
        "rating": 5,
        "comment": "Отличный ноутбук для работы с графикой и программирования!",
        "pros": ["Производительность", "Качество экрана", "Время работы"],
        "cons": ["Высокая цена"],
        "created_at": datetime.now(UTC)
    },
    {
        "laptop_name": "Dell XPS 15",
        "user_username": "alice_smith",
        "rating": 4,
        "comment": "Хороший баланс цены и качества",
        "pros": ["Мощная видеокарта", "Большой SSD"],
        "cons": ["Шумные вентиляторы"],
        "created_at": datetime.now(UTC)
    },
    {
        "laptop_name": "ThinkPad X1 Carbon",
        "user_username": "john_doe",
        "rating": 4.5,
        "comment": "Идеальный бизнес-ноутбук",
        "pros": ["Легкий вес", "Отличная клавиатура"],
        "cons": ["Слабая игровая производительность"],
        "created_at": datetime.now(UTC)
    }
]

# Добавление данных в базу
user_result = db.users.insert_many(users)
laptop_result = db.laptops.insert_many(laptops)
review_result = db.reviews.insert_many(reviews)

# Создание индексов для оптимизации запросов
db.laptops.create_index("name")
db.laptops.create_index("brand")
db.laptops.create_index("price")
db.users.create_index("username", unique=True)
db.users.create_index("email", unique=True)
db.reviews.create_index([("laptop_name", 1), ("user_username", 1)])

# Вывод результатов
print(f"Добавлено {len(user_result.inserted_ids)} пользователей")
print(f"Добавлено {len(laptop_result.inserted_ids)} ноутбуков")
print(f"Добавлено {len(review_result.inserted_ids)} отзывов")

# Проверка данных
print("\nПользователи:")
for user in db.users.find({}, {"username": 1, "email": 1}):
    print(f"- {user['username']} ({user['email']})")

print("\nНоутбуки:")
for laptop in db.laptops.find():
    print(f"- {laptop['name']} ({laptop['brand']}) - ${laptop['price']}")

print("\nОтзывы:")
for review in db.reviews.find():
    print(f"- {review['laptop_name']} | Оценка: {review['rating']} | Автор: {review['user_username']}") 