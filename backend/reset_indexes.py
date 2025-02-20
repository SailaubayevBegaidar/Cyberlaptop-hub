from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['find_best_laptop']

# Удаление всех индексов из коллекции users
db.users.drop_indexes()

# Создание новых индексов
db.users.create_index("username", unique=True)
db.users.create_index("email", unique=True)

print("Индексы успешно обновлены") 