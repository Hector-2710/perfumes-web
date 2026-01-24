# 🌸 Essenciarabe - Perfume E-commerce Platform

> A modern, automated perfume e-commerce platform with WhatsApp integration for seamless customer experience.

## 📋 Overview

Essenciarabe is a full-featured e-commerce API designed for selling sealed perfumes and 5ml decants (samples). The platform automates customer interactions through WhatsApp integration, reducing manual workload while providing real-time inventory management and a smooth shopping experience.

## ✨ Features

### Core Functionality
- 🛍️ **Product Catalog**: Browse sealed perfumes and decants with detailed information
- 🛒 **Shopping Cart**: Add, update, and remove items seamlessly
- 👤 **User Management**: Complete CRUD operations for user accounts
- 💬 **WhatsApp Integration**: Direct checkout and automated customer support
- 📊 **Real-time Inventory**: Live stock tracking to prevent overselling
- 🔐 **Secure Authentication**: JWT-based authentication system

### Business Features
- 📦 **Product Categories**: Organize by fragrance families, brands, and types
- 💰 **Dynamic Pricing**: Support for discounts and bundle offers
- 🔔 **Notifications**: Stock alerts and order updates
- ⏰ **Reservation System**: Hold stock during checkout process

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 (Async with asyncpg)
- **ORM**: SQLModel (SQLAlchemy 2.0 + Pydantic V2)
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic V2 (via SQLModel)
- **Migration**: Alembic

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Cache**: Redis (for sessions and rate limiting)
- **Message Queue**: Celery (for async tasks)
- **WhatsApp API**: Twilio / WhatsApp Business API

### Development Tools
- **Testing**: Pytest, Pytest-asyncio
- **Code Quality**: Ruff, Black, MyPy
- **Documentation**: Swagger/OpenAPI (auto-generated)
- **Load Testing**: Locust

## 📁 Project Structure

```
Essenciarabe/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration and environment variables
│   ├── database.py             # Database connection and session management
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   │
│   ├── schemas/                # Pydantic schemas for validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   │
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (auth, db session)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── products.py
│   │       ├── cart.py
│   │       └── orders.py
│   │
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   └── whatsapp_service.py
│   │
│   ├── core/                   # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py         # Password hashing, JWT
│   │   └── exceptions.py       # Custom exceptions
│   │
│   └── utils/                  # Helper functions
│       ├── __init__.py
│       └── validators.py
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_products.py
│   └── test_cart.py
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── scripts/                    # Utility scripts
│   ├── seed_data.py            # Populate database with sample data
│   └── init_db.py              # Initialize database
│
├── docker/                     # Docker configurations
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env.example                # Environment variables template
├── .gitignore
├── requirements.txt            # Python dependencies
├── pyproject.toml              # Project configuration
├── alembic.ini                 # Alembic configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for local development)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Essenciarabe.git
cd Essenciarabe
```

2. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start with Docker** (Recommended)
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose exec api alembic upgrade head
```

5. **Seed initial data** (Optional)
```bash
docker-compose exec api python scripts/seed_data.py
```

6. **Access the API**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Local Development (Without Docker)

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start PostgreSQL** (ensure it's running locally or via Docker)
```bash
docker run -d \
  --name essenciarabe-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=essenciarabe \
  -p 5432:5432 \
  postgres:15
```

4. **Run migrations**
```bash
alembic upgrade head
```

5. **Start the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

### Authentication
All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Main Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token

#### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user
- `GET /api/v1/users/{user_id}` - Get user by ID (admin)
- `GET /api/v1/users` - List all users (admin)

#### Products
- `GET /api/v1/products` - List all products (with filters)
- `GET /api/v1/products/{product_id}` - Get product details
- `POST /api/v1/products` - Create product (admin)
- `PUT /api/v1/products/{product_id}` - Update product (admin)
- `DELETE /api/v1/products/{product_id}` - Delete product (admin)

#### Shopping Cart
- `GET /api/v1/cart` - Get current user's cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{item_id}` - Update cart item quantity
- `DELETE /api/v1/cart/items/{item_id}` - Remove item from cart
- `DELETE /api/v1/cart` - Clear cart

#### Orders
- `POST /api/v1/orders/checkout` - Checkout and generate WhatsApp message
- `GET /api/v1/orders` - Get user's order history
- `GET /api/v1/orders/{order_id}` - Get order details

For detailed API documentation, visit `/docs` when the server is running.

## 🧪 Testing

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_auth.py -v
```

### Load testing
```bash
locust -f tests/load_test.py
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v

# Access API container shell
docker-compose exec api bash

# Run database migrations
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"
```

## 🔧 Configuration

Key environment variables (see `.env.example`):

```env
# Application
APP_NAME=Essenciarabe
DEBUG=False
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/essenciarabe

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# WhatsApp API
WHATSAPP_API_KEY=your-api-key
WHATSAPP_PHONE_NUMBER=+1234567890

# Redis
REDIS_URL=redis://localhost:6379/0
```

## 📈 Roadmap

- [x] Core API structure
- [x] User authentication & management
- [x] Product catalog
- [x] Shopping cart functionality
- [ ] WhatsApp integration
- [ ] Automated bot responses
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Mobile app (React Native)
- [ ] Analytics dashboard
- [ ] Loyalty program

## 🤝 Contributing

This is a personal project, but suggestions are welcome! Please open an issue to discuss proposed changes.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Hector** - Civil Computer Engineering Student
- Specializing in REST APIs (FastAPI)
- Database expertise (PostgreSQL, MongoDB)
- Perfume enthusiast and entrepreneur

## 🙏 Acknowledgments

- FastAPI framework and community
- SQLAlchemy ORM
- All open-source contributors

---

**Note**: This project is designed to automate customer interactions and reduce manual workload for a perfume business while maintaining a professional and scalable architecture.
