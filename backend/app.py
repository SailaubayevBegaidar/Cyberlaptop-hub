from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from config import Config
from models import User, Laptop
import bcrypt
from bson import ObjectId
from datetime import datetime, UTC
from pymongo import ASCENDING, DESCENDING

app = Flask(__name__, 
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)
app.config.from_object(Config)

mongo = PyMongo(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)
login_manager.login_view = 'login'

try:
    # Проверка подключения
    mongo.db.command('ping')
    print("Подключение к MongoDB успешно!")
    
    # Вывод списка всех коллекций
    print("Доступные коллекции:", mongo.db.list_collection_names())
    
    # Проверка количества документов в коллекциях
    print("Количество пользователей:", mongo.db.users.count_documents({}))
    print("Количество ноутбуков:", mongo.db.laptops.count_documents({}))
    print("Количество отзывов:", mongo.db.reviews.count_documents({}))

except Exception as e:
    print("Ошибка подключения к MongoDB:", e)

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_data) if user_data else None

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'price')
    sort_order = request.args.get('order', 'asc')
    
    # Использование индексов для сортировки
    sort_direction = ASCENDING if sort_order == 'asc' else DESCENDING
    laptops = mongo.db.laptops.find().sort(sort_by, sort_direction)
    
    return render_template('index.html', laptops=laptops)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = mongo.db.users.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user_model = User(user)
            login_user(user_model)
            
            # Создание JWT токенов
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            # Сохранение токенов в сессии
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token

            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Очистка токенов из сессии
    session.pop('access_token', None)
    session.pop('refresh_token', None)
    return redirect(url_for('index'))

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_data = {
        'username': username,
        'password': hashed_password
    }
    mongo.db.users.insert_one(user_data)

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'username': username
    }), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'username': username
        })
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token})

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'logged_in_as': current_user})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Проверка существования пользователя
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('register'))

        # Проверка существования email
        if mongo.db.users.find_one({'email': email}):
            flash('Email already exists')
            return redirect(url_for('register'))

        # Проверка совпадения паролей
        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        # Хеширование пароля и создание пользователя
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password,
            'created_at': datetime.now(UTC)
        }
        
        try:
            # Добавление пользователя в базу данных
            mongo.db.users.insert_one(user_data)
            
            # Получение созданного пользователя
            user = mongo.db.users.find_one({'username': username})
            user_model = User(user)
            login_user(user_model)

            # Создание JWT токенов
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)

            # Сохранение токенов в сессии
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token

            flash('Registration successful!')
            return redirect(url_for('index'))
        except Exception as e:
            flash('An error occurred during registration')
            print(f"Error: {e}")
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/admin')
@login_required
def admin():
    # Проверка, является ли пользователь администратором
    if not current_user.is_admin:
        abort(403)  # Forbidden
    laptops = mongo.db.laptops.find()
    return render_template('admin.html', laptops=laptops)

@app.route('/admin/laptop/add', methods=['POST'])
@login_required
def admin_laptop_add():
    if not current_user.is_admin:
        abort(403)

    laptop_data = {
        'name': request.form['name'],
        'brand': request.form['brand'],
        'price': float(request.form['price']),
        'specs': {
            'processor': request.form['specs[processor]'],
            'ram': request.form['specs[ram]'],
            'storage': request.form['specs[storage]'],
            'display': request.form['specs[display]'],
            'gpu': request.form['specs[gpu]']
        },
        'in_stock': 'in_stock' in request.form,
        'created_at': datetime.now(UTC)
    }

    mongo.db.laptops.insert_one(laptop_data)
    flash('Laptop added successfully!')
    return redirect(url_for('admin'))

@app.route('/admin/laptop/edit/<laptop_id>', methods=['GET', 'POST'])
@login_required
def admin_laptop_edit(laptop_id):
    if not current_user.is_admin:
        abort(403)

    laptop = mongo.db.laptops.find_one({'_id': ObjectId(laptop_id)})
    if not laptop:
        abort(404)

    if request.method == 'POST':
        updated_data = {
            'name': request.form['name'],
            'brand': request.form['brand'],
            'price': float(request.form['price']),
            'specs': {
                'processor': request.form['specs[processor]'],
                'ram': request.form['specs[ram]'],
                'storage': request.form['specs[storage]'],
                'display': request.form['specs[display]'],
                'gpu': request.form['specs[gpu]']
            },
            'in_stock': 'in_stock' in request.form
        }

        mongo.db.laptops.update_one(
            {'_id': ObjectId(laptop_id)},
            {'$set': updated_data}
        )
        flash('Laptop updated successfully!')
        return redirect(url_for('admin'))

    return render_template('admin.html', edit_laptop=laptop, laptops=mongo.db.laptops.find())

@app.route('/admin/laptop/delete/<laptop_id>', methods=['POST'])
@login_required
def admin_laptop_delete(laptop_id):
    if not current_user.is_admin:
        abort(403)

    mongo.db.laptops.delete_one({'_id': ObjectId(laptop_id)})
    flash('Laptop deleted successfully!')
    return redirect(url_for('admin'))

@app.route('/api/laptops/search')
def search_laptops():
    query = request.args.get('q', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    brand = request.args.get('brand', '')
    in_stock = request.args.get('in_stock', type=bool)

    search_query = {}
    
    # Текстовый поиск
    if query:
        search_query['$text'] = {'$search': query}
    
    # Фильтры
    if brand:
        search_query['brand'] = brand
    if min_price is not None or max_price is not None:
        search_query['price'] = {}
        if min_price is not None:
            search_query['price']['$gte'] = min_price
        if max_price is not None:
            search_query['price']['$lte'] = max_price
    if in_stock is not None:
        search_query['in_stock'] = in_stock

    try:
        # Используем соответствующий индекс в зависимости от параметров
        if query:
            results = mongo.db.laptops.find(
                search_query,
                {'score': {'$meta': 'textScore'}}
            ).sort([('score', {'$meta': 'textScore'})])
        elif brand and (min_price is not None or max_price is not None):
            results = mongo.db.laptops.find(search_query).hint('brand_price_index')
        elif min_price is not None or max_price is not None:
            results = mongo.db.laptops.find(search_query).hint('price_index')
        else:
            results = mongo.db.laptops.find(search_query)

        laptops = list(results)
        return jsonify([{**laptop, '_id': str(laptop['_id'])} for laptop in laptops])
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/laptops/filter')
def filter_laptops():
    """Оптимизированная фильтрация и сортировка"""
    # Получение параметров фильтрации
    brand = request.args.get('brand')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    in_stock = request.args.get('in_stock', type=bool)
    sort_by = request.args.get('sort', 'price')
    sort_order = request.args.get('order', 'asc')

    # Построение фильтра
    filter_query = {}
    if brand:
        filter_query['brand'] = brand
    if min_price is not None or max_price is not None:
        price_query = {}
        if min_price is not None:
            price_query['$gte'] = min_price
        if max_price is not None:
            price_query['$lte'] = max_price
        if price_query:
            filter_query['price'] = price_query
    if in_stock is not None:
        filter_query['in_stock'] = in_stock

    # Определение сортировки
    sort_direction = ASCENDING if sort_order == 'asc' else DESCENDING
    
    # Выполнение оптимизированного запроса
    results = mongo.db.laptops.find(
        filter_query
    ).sort(sort_by, sort_direction).hint(f"{sort_by}_index")

    laptops = list(results)
    return jsonify([{**laptop, '_id': str(laptop['_id'])} for laptop in laptops])

@app.route('/api/laptops/stats')
def laptop_stats():
    """Агрегированная статистика"""
    pipeline = [
        {
            "$group": {
                "_id": "$brand",
                "count": {"$sum": 1},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"}
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    
    stats = list(mongo.db.laptops.aggregate(pipeline))
    return jsonify(stats)

@app.route('/laptop/<laptop_id>')
def laptop_detail(laptop_id):
    laptop = mongo.db.laptops.find_one({'_id': ObjectId(laptop_id)})
    if not laptop:
        abort(404)
    
    # Получаем отзывы для этого ноутбука
    reviews = list(mongo.db.reviews.find({'laptop_id': ObjectId(laptop_id)}).sort('created_at', -1))
    
    return render_template('laptop_detail.html', laptop=laptop, reviews=reviews)

@app.route('/laptop/<laptop_id>/review', methods=['POST'])
@login_required
def add_review(laptop_id):
    laptop = mongo.db.laptops.find_one({'_id': ObjectId(laptop_id)})
    if not laptop:
        abort(404)
    
    # Проверяем, не оставлял ли пользователь уже отзыв
    existing_review = mongo.db.reviews.find_one({
        'laptop_id': ObjectId(laptop_id),
        'user_username': current_user.username
    })
    
    if existing_review:
        flash('You have already reviewed this laptop')
        return redirect(url_for('laptop_detail', laptop_id=laptop_id))
    
    # Создаем новый отзыв
    review_data = {
        'laptop_id': ObjectId(laptop_id),
        'laptop_name': laptop['name'],
        'user_username': current_user.username,
        'rating': int(request.form['rating']),
        'comment': request.form['comment'],
        'pros': [pro.strip() for pro in request.form['pros'].split(',') if pro.strip()],
        'cons': [con.strip() for con in request.form['cons'].split(',') if con.strip()],
        'created_at': datetime.now(UTC)
    }
    
    # Сохраняем отзыв в базе данных
    mongo.db.reviews.insert_one(review_data)
    
    # Обновляем средний рейтинг ноутбука
    all_reviews = mongo.db.reviews.find({'laptop_id': ObjectId(laptop_id)})
    ratings = [r['rating'] for r in all_reviews]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    mongo.db.laptops.update_one(
        {'_id': ObjectId(laptop_id)},
        {'$set': {'avg_rating': avg_rating}}
    )
    
    flash('Your review has been added successfully!')
    return redirect(url_for('laptop_detail', laptop_id=laptop_id))

if __name__ == '__main__':
    app.run(debug=True) 