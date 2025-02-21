from pymongo import MongoClient
from datetime import datetime
import random
from bson import ObjectId

# Подключение к MongoDB
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['find_best_laptop']  # Используем правильное имя базы данных

print("Connected to MongoDB...")

try:
    # Проверка подключения
    client.server_info()
    print("Successfully connected to MongoDB!")

    # Очистка существующей коллекции
    result = db.laptops.delete_many({})
    print(f"Cleared {result.deleted_count} existing laptops")

    # Данные для генерации
    brands = ['Asus', 'Lenovo', 'Dell', 'HP', 'Acer', 'MSI', 'Apple', 'Razer', 'Samsung', 'LG']
    models = ['Pro', 'Elite', 'Gaming', 'Creator', 'Ultra', 'Book', 'Station', 'Studio']
    processor_brands = ['Intel', 'AMD', 'Apple']
    processor_series = {
        'Intel': ['i3', 'i5', 'i7', 'i9'],
        'AMD': ['Ryzen 3', 'Ryzen 5', 'Ryzen 7', 'Ryzen 9'],
        'Apple': ['M1', 'M1 Pro', 'M1 Max', 'M2', 'M2 Pro', 'M2 Max']
    }
    ram_sizes = ['8GB', '16GB', '32GB', '64GB']
    storage_types = ['256GB SSD', '512GB SSD', '1TB SSD', '2TB SSD']
    display_sizes = ['13.3"', '14"', '15.6"', '16"', '17.3"']
    display_types = ['FHD', '2K', '4K', 'Retina', 'OLED', 'Mini-LED']
    gpu_brands = {
        'NVIDIA': ['RTX 3050', 'RTX 3060', 'RTX 3070', 'RTX 3080', 'RTX 4060', 'RTX 4070', 'RTX 4080', 'RTX 4090'],
        'AMD': ['RX 6600M', 'RX 6700M', 'RX 6800M'],
        'Apple': ['M1 GPU', 'M2 GPU'],
        'Intel': ['Intel Iris Xe', 'Intel UHD']
    }

    laptops_to_add = []

    # Добавляем MacBook Pro 16 как первый ноутбук
    macbook = {
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
        "created_at": datetime.now()
    }
    laptops_to_add.append(macbook)

    # Генерация остальных 49 ноутбуков
    for i in range(49):
        brand = random.choice(brands)
        model = random.choice(models)
        series_number = random.randint(1, 9)
        
        if brand == 'Apple':
            processor_brand = 'Apple'
            gpu_brand = 'Apple'
        else:
            processor_brand = random.choice(['Intel', 'AMD'])
            gpu_brand = random.choice(['NVIDIA', 'AMD', 'Intel'])

        processor = f"{processor_brand} {random.choice(processor_series[processor_brand])}"
        if processor_brand in ['Intel', 'AMD']:
            processor += f" {random.randint(10000, 13999)}"

        gpu = random.choice(gpu_brands[gpu_brand])

        base_price = random.randint(800, 3000)
        if 'RTX 40' in gpu or 'M2 Max' in processor:
            base_price += 1000
        if '32GB' in ram_sizes or '64GB' in ram_sizes:
            base_price += 500

        laptop = {
            "name": f"{brand} {model} {series_number}",
            "brand": brand,
            "price": base_price,
            "specs": {
                "processor": processor,
                "ram": random.choice(ram_sizes),
                "storage": random.choice(storage_types),
                "display": f"{random.choice(display_sizes)} {random.choice(display_types)}",
                "gpu": gpu
            },
            "in_stock": random.choice([True, True, True, False]),
            "created_at": datetime.now()
        }
        laptops_to_add.append(laptop)

    # Добавление всех ноутбуков в базу данных
    result = db.laptops.insert_many(laptops_to_add)
    print(f"Successfully added {len(result.inserted_ids)} laptops to the database!")

    # Проверка добавленных ноутбуков
    count = db.laptops.count_documents({})
    print(f"\nTotal laptops in database: {count}")
    
    print("\nExample of added laptops:")
    for laptop in db.laptops.find().limit(3):
        print(f"\nName: {laptop['name']}")
        print(f"Brand: {laptop['brand']}")
        print(f"Price: ${laptop['price']}")
        print("Specs:", laptop['specs'])
        print(f"In Stock: {laptop['in_stock']}")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
    print("MongoDB connection closed") 