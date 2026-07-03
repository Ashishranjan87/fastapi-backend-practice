# FastAPI Backend Practice

A collection of backend development exercises and mini-projects built with **FastAPI** to practice REST API development, authentication, database integration, validation, and backend best practices.

This repository serves as a hands-on learning project for building production-ready backend applications using modern Python technologies.

---

## Objectives

* Learn FastAPI fundamentals and advanced concepts
* Build RESTful APIs following clean architecture principles
* Practice database integration with SQLAlchemy
* Implement secure authentication using JWT
* Improve API validation, error handling, and project organization

---

## Tech Stack

| Technology          | Purpose                       |
| ------------------- | ----------------------------- |
| Python 3            | Programming Language          |
| FastAPI             | Web Framework                 |
| SQLAlchemy          | ORM                           |
| PostgreSQL / SQLite | Database                      |
| Pydantic            | Request & Response Validation |
| Alembic             | Database Migrations           |
| JWT                 | Authentication                |
| BCrypt              | Password Hashing              |
| Uvicorn             | ASGI Server                   |

---

## Topics Covered

* FastAPI Routing
* Request & Response Models
* CRUD Operations
* Dependency Injection
* JWT Authentication
* Password Hashing
* Database Relationships
* Pagination
* Filtering & Searching
* Error Handling
* Middleware
* Environment Variables
* Database Migrations
* Modular Project Structure
* API Documentation with Swagger

---

## Project Structure

```text
fastapi-backend-practice/
│
├── app/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── database/
│   ├── core/
│   └── utils/
│
├── alembic/
├── tests/
├── requirements.txt
├── main.py
└── README.md
```

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Ashishranjan87/fastapi-backend-practice.git
cd fastapi-backend-practice
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Environment

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Apply Database Migrations

```bash
alembic upgrade head
```

### Run the Application

```bash
uvicorn main:app --reload
```

---

## API Documentation

Once the application is running:

**Swagger UI**

```text
http://localhost:8000/docs
```

**ReDoc**

```text
http://localhost:8000/redoc
```

---

## Example Features

* User Registration & Login
* JWT Authentication
* CRUD APIs
* Product APIs
* Category APIs
* Database Relationships
* Input Validation
* Exception Handling
* Pagination & Filtering

---

## Future Improvements

* Async SQLAlchemy
* Redis Caching
* Background Tasks
* Docker Support
* Unit & Integration Tests
* GitHub Actions CI/CD
* Role-Based Access Control (RBAC)
* API Rate Limiting
* Logging & Monitoring
* AWS Deployment

---

## Skills Demonstrated

* Python Backend Development
* FastAPI Framework
* REST API Design
* SQLAlchemy ORM
* Authentication & Authorization
* Database Design
* Clean Project Structure
* API Validation
* Error Handling
* Backend Best Practices

---

## License

This project is intended for learning, experimentation, and portfolio purposes.
