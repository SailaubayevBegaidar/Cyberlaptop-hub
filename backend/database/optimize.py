from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.operations import IndexModel

def setup_indexes():
    # Подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['find_best_laptop']

    try:
        # Сначала удалим все существующие индексы (кроме _id)
        print("Удаление существующих индексов...")
        db.laptops.drop_indexes()
        db.users.drop_indexes()
        db.reviews.drop_indexes()
        print("Существующие индексы удалены")

        # Создание новых индексов для коллекции laptops
        print("Создание новых индексов...")
        laptop_indexes = [
            # Полнотекстовый поиск по всем важным полям
            IndexModel([
                ("name", TEXT), 
                ("brand", TEXT),
                ("specs.processor", TEXT),
                ("specs.gpu", TEXT),
                ("specs.ram", TEXT)
            ], name="full_text_search"),
            
            # Составные индексы для фильтрации и сортировки
            IndexModel([("brand", ASCENDING), ("price", ASCENDING)], 
                      name="brand_price_index"),
            IndexModel([("price", ASCENDING)], 
                      name="price_index"),
            IndexModel([("in_stock", ASCENDING), ("price", ASCENDING)], 
                      name="stock_price_index"),
            
            # Индексы для спецификаций
            IndexModel([("specs.processor", ASCENDING)], 
                      name="processor_index"),
            IndexModel([("specs.ram", ASCENDING)], 
                      name="ram_index"),
            IndexModel([("specs.gpu", ASCENDING)], 
                      name="gpu_index")
        ]
        db.laptops.create_indexes(laptop_indexes)
        print("Индексы для laptops созданы")

        # Индексы для коллекции users
        user_indexes = [
            IndexModel([("username", ASCENDING)], unique=True, 
                      name="username_index"),
            IndexModel([("email", ASCENDING)], unique=True, 
                      name="email_index")
        ]
        db.users.create_indexes(user_indexes)
        print("Индексы для users созданы")

        # Индексы для коллекции reviews
        review_indexes = [
            IndexModel([("laptop_name", ASCENDING)], 
                      name="laptop_review_index"),
            IndexModel([("user_username", ASCENDING)], 
                      name="user_review_index"),
            IndexModel([("rating", DESCENDING)], 
                      name="rating_index")
        ]
        db.reviews.create_indexes(review_indexes)
        print("Индексы для reviews созданы")

        print("\nВсе индексы успешно обновлены!")

        # Вывод информации о созданных индексах
        print("\nТекущие индексы в коллекции laptops:")
        for index in db.laptops.list_indexes():
            print(index)

        print("\nТекущие индексы в коллекции users:")
        for index in db.users.list_indexes():
            print(index)

        print("\nТекущие индексы в коллекции reviews:")
        for index in db.reviews.list_indexes():
            print(index)

    except Exception as e:
        print(f"Ошибка при создании индексов: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    setup_indexes() 