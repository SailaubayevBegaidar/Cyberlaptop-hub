<div align="center">
  <h1>🌟 CyberLaptop Hub 🌟</h1>
  <p>A modern web application for browsing and reviewing laptops with a cyberpunk-themed design</p>

  ![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
  ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)
  ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb)
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3)
  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript)
</div>

---

## 📚 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Security Features](#-security-features)
- [Contributing](#-contributing)
- [Database Schema](#-database-schema)

## ✨ Features

### 🎨 Frontend
- **Cyberpunk Design**
  - Neon effects and animations
  - Responsive layout
  - Interactive UI elements
- **User Features**
  - Authentication system
  - Laptop catalog
  - Review system
  - Rating system
- **Admin Panel**
  - Laptop management
  - User management
  - Statistics dashboard

### 🔧 Backend
- **API System**
  - RESTful architecture
  - JWT authentication
  - Role-based access
- **Database**
  - MongoDB integration
  - Optimized queries
  - Data indexing
- **Security**
  - Password hashing
  - Protected routes
  - Input validation

## 🛠 Tech Stack

<details>
<summary>Frontend Technologies</summary>

- HTML5/CSS3
- JavaScript
- Custom animations
- Rajdhani font
- Responsive design
</details>

<details>
<summary>Backend Technologies</summary>

- Python 3.x
- Flask framework
- PyMongo
- JWT
- BCrypt
- MongoDB
</details>

## 📦 Installation

1. **Clone Repository**
```bash
git clone https://github.com/SailaubayevBegaidar/Cyberlaptop-hub
cd cyberlaptop-hub
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Environment Setup**
Create `.env` file:
```env
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017/find_best_laptop
JWT_SECRET_KEY=your_jwt_secret
```

5. **Initialize Database**
```bash
# Start MongoDB
mongod

# Setup database
python database/optimize.py
python create_admin.py
python seed_data.py
```

## 🚀 Running the Application

1. **Start MongoDB**
```bash
mongod
```

2. **Launch Server**
```bash
cd backend
python app.py
```

3. **Access Application**
- 🌐 Main site: `http://localhost:5000`
- 👑 Admin panel: `http://localhost:5000/admin`

### 👤 Default Admin Access
```
Username: admin
Password: admin123
```

## 📡 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | User login |
| POST | `/api/refresh` | Refresh JWT token |

### 💻 Laptops
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/laptops` | Get all laptops |
| GET | `/api/laptops/search` | Search laptops |
| GET | `/api/laptops/filter` | Filter laptops |
| GET | `/api/laptops/stats` | Get statistics |

### ⭐ Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/laptop/<id>/review` | Add review |
| GET | `/laptop/<id>` | Get laptop details |

## 📂 Project Structure

### Frontend
```
frontend/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin.html
│   └── laptop_detail.html
├── static/
│   ├── style.css
│   └── js/
│       ├── auth.js
│       ├── forms.js
│       ├── search.js
│       └── cyber-effects.js
```

### Backend
```
backend/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── create_admin.py
└── database/
    ├── optimize.py
    └── seed_data.py
```



### 📊 Collections

#### Users Collection
```json
{
    "_id": ObjectId,
    "username": String,
    "email": String,
    "password": String (hashed),
    "is_admin": Boolean,
    "created_at": DateTime,
    "last_login": DateTime
}
```

#### Laptops Collection
```json
{
    "_id": ObjectId,
    "name": String,
    "brand": String,
    "price": Number,
    "specs": {
        "processor": String,
        "ram": String,
        "storage": String,
        "display": String,
        "gpu": String
    },
    "in_stock": Boolean,
    "avg_rating": Number,
    "review_count": Number,
    "created_at": DateTime,
    "updated_at": DateTime
}
```

#### Reviews Collection
```json
{
    "_id": ObjectId,
    "laptop_id": ObjectId,
    "user_username": String,
    "rating": Number (1-5),
    "comment": String,
    "pros": Array[String],
    "cons": Array[String],
    "created_at": DateTime
}
```

### 🔗 Relationships
- Reviews.laptop_id → Laptops._id
- Reviews.user_username → Users.username

### 📑 Indexes
- Users Collection:
  - `username` (unique)
  - `email` (unique)
- Laptops Collection:
  - `name` (text)
  - `brand` (text)
  - `price` (ascending)
  - `avg_rating` (descending)
- Reviews Collection:
  - `laptop_id` (ascending)
  - `user_username` (ascending)
  - `rating` (descending)


## 🔒 Security Features
- BCrypt password hashing
- JWT authentication
- Protected admin routes
- CSRF protection
- Input validation

## 🌐 Browser Support
![Chrome](https://img.shields.io/badge/Chrome-Latest-green)
![Firefox](https://img.shields.io/badge/Firefox-Latest-orange)
![Safari](https://img.shields.io/badge/Safari-Latest-blue)
![Edge](https://img.shields.io/badge/Edge-Latest-blue)

## 📱 Responsive Design
- Mobile-first approach
- Tablet optimization
- Desktop enhancement
- Dynamic layouts

## 🤝 Contributing

1. Fork repository
2. Create feature branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit changes
```bash
git commit -m 'Add AmazingFeature'
```
4. Push to branch
```bash
git push origin feature/AmazingFeature
```
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">
  <p>Made with ❤️</p>
  <p>
    <a href="https://github.com/yourusername">Github</a> •
    <a href="https://linkedin.com/in/yourusername">LinkedIn</a>
  </p>
</div>