# 🌸 Essenciarabe - Perfume E-commerce Platform

> A modern, automated perfume e-commerce platform with WhatsApp integration for seamless customer experience.

## 📋 Overview

Essenciarabe is a full-featured e-commerce platform designed for selling sealed perfumes and 5ml decants (samples). The project is divided into a robust **FastAPI** backend and a high-performance **Astro** frontend, both containerized for easy deployment. It automates customer interactions through WhatsApp integration, providing real-time inventory management and a smooth shopping experience.

## ✨ Features

### Core Functionality
- 🛍️ **Product Catalog**: Browse sealed perfumes and decants with detailed information.
- 🛒 **Shopping Cart**: Add, update, and remove items seamlessly.
- 👤 **User Management**: Complete CRUD operations for user accounts.
- 💬 **WhatsApp Integration**: Direct checkout and automated customer support.
- 📊 **Real-time Inventory**: Live stock tracking to prevent overselling.
- 🔐 **Secure Authentication**: JWT-based authentication system.

### Business Features
- 📦 **Product Categories**: Organize by fragrance families, brands, and types.
- 💰 **Dynamic Pricing**: Support for discounts and bundle offers.
- 🔔 **Notifications**: Stock alerts and order updates.
- ⏰ **Reservation System**: Hold stock during checkout process.

## 🏗️ Technology Stack

### Frontend
- **Framework**: [Astro 5](https://astro.build/)
- **Styling**: Vanilla CSS (Modern design)
- **Deployment**: SSR/Static

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 (Async with asyncpg)
- **ORM**: SQLModel (SQLAlchemy 2.0 + Pydantic V2)
- **Authentication**: JWT (python-jose)
- **Validation**: Pydantic V2 
- **Caching**: Redis (Sessions & Rate limiting)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Message Queue**: Celery (Async tasks)
- **WhatsApp API**: Twilio / WhatsApp Business API

## 📁 Project Structure

```text
Essenciarabe/
├── backend/                # FastAPI Application
│   ├── app/                # Core logic, models, api
│   ├── scripts/            # Database initialization/seeding
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── frontend/               # Astro Application
│   ├── src/                # Pages, Components, Layouts
│   ├── public/             # Static assets
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml      # Orchestration
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hector-2710/perfumes-web.git
cd Essenciarabe
```

2. **Configure environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. **Start the whole stack with Docker**
```bash
docker-compose up --build -d
```

4. **Run database migrations & seed data**
```bash
docker-compose exec api alembic upgrade head
docker-compose exec api python backend/scripts/seed_data.py
```

5. **Access the services**
- **Frontend**: [http://localhost:4321](http://localhost:4321)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **pgAdmin**: [http://localhost:5050](http://localhost:5050)

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f
docker-compose logs -f api
docker-compose logs -f frontend

# Stop all services
docker-compose down
```

## 🔧 Configuration

Key environment variables in `backend/.env`:
- `DATABASE_URL`: PostgreSQL connection string.
- `SECRET_KEY`: Security key for JWT tokens.
- `REDIS_URL`: Redis connection string.
- `WHATSAPP_PHONE_NUMBER`: Target number for order messages.

## 📈 Roadmap

- [x] Core API structure
- [x] User authentication & management
- [x] Product catalog
- [x] Shopping cart functionality
- [x] Reorganized Backend/Frontend structure
- [x] Astro frontend initial setup
- [ ] WhatsApp integration
- [ ] Automated bot responses
- [ ] Payment gateway integration

## 👨‍💻 Author

**Hector** - Civil Computer Engineering Student
- Specializing in REST APIs (FastAPI) & Databases.
- Perfume enthusiast and entrepreneur.

---

**Note**: This project is designed to automate customer interactions and reduce manual workload for a perfume business while maintaining a professional and scalable architecture.
