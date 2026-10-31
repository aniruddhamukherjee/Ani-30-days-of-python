# Enterprise Products API

A high-performance, asynchronous REST API built with **FastAPI**, **SQLAlchemy 2.0 (asyncpg)**, and **PostgreSQL**. Designed using clean enterprise architecture patterns with full support for PostgreSQL advanced data types like `UUID`, `JSONB`, and `text[]` arrays.

---

## 📋 Table of Contents
- [Architecture Overview](#-architecture-overview)
- [Database Schema](#-database-schema)
- [Prerequisites](#-prerequisites)
- [How to Run](#-how-to-run)
  - [Option 1: Run Locally with Python Virtualenv](#option-1-run-locally-with-python-virtualenv)
  - [Option 2: Run with Docker Compose](#option-2-run-with-docker-compose)
- [Testing & Using with Postman](#-testing--using-with-postman)
  - [Method 1: One-Click Postman OpenAPI Import (Fastest)](#method-1-one-click-postman-openapi-import-fastest)
  - [Method 2: Manual Postman Requests](#method-2-manual-postman-requests)
- [Interactive Swagger & ReDoc Documentation](#-interactive-swagger--redoc-documentation)
- [Running Tests](#-running-tests)
- [Useful Understanding Notes](#-useful-understanding-notes)

---

## 🏛 Architecture Overview

```text
my_enterprise_api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # App initialization, CORS & lifespan
│   ├── core/                       # Global configs & database engine
│   │   ├── config.py               # Pydantic Settings (.env support)
│   │   ├── database.py             # Async SQLAlchemy session lifecycle
│   │   └── security.py             # Security utilities
│   ├── exceptions/                 # Global exception handlers
│   │   └── __init__.py
│   ├── api/                        # API version routing
│   │   └── v1/
│   │       ├── api.py              # Feature router aggregator
│   │       └── endpoints/
│   │           └── products.py     # Product CRUD endpoints
│   ├── models/                     # SQLAlchemy ORM Models
│   │   └── __init__.py
│   ├── schemas/                    # Pydantic validation schemas
│   │   └── __init__.py
│   └── services/                   # Business logic layer
│       └── __init__.py
├── migrations/                     # Alembic database migrations
├── tests/                          # Automated Pytest suite
├── .env                            # Environment variables
├── Dockerfile                      # Production multi-stage Dockerfile
├── docker-compose.yml              # Local orchestration stack
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation
```

---

## 🗄 Database Schema

The API connects to PostgreSQL and interacts with the **`products`** table:

| Column | Type | Nullable | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| `product_id` | `uuid` | ❌ No | `gen_random_uuid()` | Primary Key |
| `sku` | `varchar(50)` | ❌ No | — | Unique Product Stock Keeping Unit |
| `name` | `text` | ❌ No | — | Product Name |
| `description` | `text` | ✔️ Yes | `NULL` | Product Details / Overview |
| `price` | `numeric(10, 2)` | ❌ No | — | Unit Price |
| `stock_quantity`| `int4` | ❌ No | `0` | Available Inventory |
| `metadata` | `jsonb` | ✔️ Yes | `'{}'::jsonb` | Attributes, specs, brand, custom data |
| `tags` | `_text` (`text[]`) | ✔️ Yes | `ARRAY[]::text[]`| Categories & search tags |
| `is_active` | `bool` | ❌ No | `true` | Product Availability Status |
| `created_at` | `timestamptz` | ❌ No | `clock_timestamp()` | Creation Timestamp |
| `updated_at` | `timestamptz` | ❌ No | `clock_timestamp()` | Auto-updated Timestamp |

---

## ⚙️ Prerequisites

1. **Python 3.11+** installed
2. **PostgreSQL** running on port `5432` (e.g., via Docker container):
   ```powershell
   docker run -d --name local-postgres -p 5432:5432 -v "D:\work\code\postgres_db_data:/var/lib/postgresql" -e POSTGRES_PASSWORD=postgres postgres:latest
   ```

---

## 🚀 How to Run

### Option 1: Run Locally with Python Virtualenv

1. **Open PowerShell and navigate to the project directory:**
   ```powershell
   cd d:\work\code\Ani-30-Days-Of-Python\python-fastapi-products-API\my_enterprise_api
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   
   # If you get an execution policy error, run this first:
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

   # Then activate the environment:
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install the dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Verify your `.env` settings:**
   Make sure `.env` points to your PostgreSQL database:
   ```env
   POSTGRES_SERVER="localhost"
   POSTGRES_PORT=5432
   POSTGRES_USER="postgres"
   POSTGRES_PASSWORD="postgres"
   POSTGRES_DB="postgres"
   ```

5. **Start the FastAPI server:**
   ```powershell
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will now be running at: **`http://localhost:8000`**

---

### Option 2: Run with Docker Compose

To run both the API and database container together:
```powershell
cd d:\work\code\Ani-30-Days-Of-Python\python-fastapi-products-API\my_enterprise_api
docker compose up --build -d
```

---

## 📮 Testing & Using with Postman

### Method 1: One-Click Postman OpenAPI Import (Fastest)

Postman can automatically generate a full collection with all endpoints, parameters, and bodies directly from FastAPI:

1. Open **Postman**.
2. Click the **Import** button (top left).
3. Paste the URL:
   ```text
   http://localhost:8000/api/v1/openapi.json
   ```
4. Click **Import**. Postman will create a collection named **`Enterprise Products API`** with every endpoint already configured!

---

### Method 2: Manual Postman Requests

#### 1. Health Check
- **Method:** `GET`
- **URL:** `http://localhost:8000/health`
- **Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "project": "Enterprise Products API",
    "api_version": "/api/v1"
  }
  ```

---

#### 2. Create a Product
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/v1/products/`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "sku": "TECH-AUD-001",
    "name": "Wireless Studio Noise-Cancelling Headphones",
    "description": "Premium over-ear headphones with 40-hour battery life and fast charging.",
    "price": 199.99,
    "stock_quantity": 45,
    "metadata": {
      "brand": "AudioTech",
      "color": "Matte Black",
      "warranty_months": 24,
      "connectivity": ["Bluetooth 5.3", "3.5mm"]
    },
    "tags": ["audio", "wireless", "electronics", "music"],
    "is_active": true
  }
  ```
- **Response (201 Created):**
  Returns the created product with its generated `product_id`, `created_at`, and `updated_at`.

---

#### 3. List Products (with Search & Pagination)
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/v1/products/`
- **Optional Query Parameters in Postman (Params tab):**
  | Key | Example Value | Description |
  | :--- | :--- | :--- |
  | `skip` | `0` | Number of records to skip |
  | `limit` | `20` | Max records to return |
  | `search` | `Headphones` | Search query matching name, SKU, or description |
  | `is_active` | `true` | Filter by active status (`true` or `false`) |
  | `tag` | `wireless` | Filter by specific tag |

---

#### 4. Get Product by UUID
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/v1/products/{product_id}`
- **Example URL:**
  ```text
  http://localhost:8000/api/v1/products/8f9b34a1-b847-49f3-8b7c-333e387192bc
  ```

---

#### 5. Get Product by SKU
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/v1/products/sku/{sku}`
- **Example URL:**
  ```text
  http://localhost:8000/api/v1/products/sku/TECH-AUD-001
  ```

---

#### 6. Update Product
- **Method:** `PUT`
- **URL:** `http://localhost:8000/api/v1/products/{product_id}`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
  ```json
  {
    "price": 179.99,
    "stock_quantity": 50,
    "is_active": true
  }
  ```

---

#### 7. Delete Product
- **Method:** `DELETE`
- **URL:** `http://localhost:8000/api/v1/products/{product_id}`
- **Response:** `204 No Content`

---

## 📖 Interactive Swagger & ReDoc Documentation

FastAPI automatically serves interactive API docs in your browser:

- **Swagger UI:** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **ReDoc:** [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)
- **OpenAPI Schema:** [http://localhost:8000/api/v1/openapi.json](http://localhost:8000/api/v1/openapi.json)

---

## 🧪 Running Tests

To run the automated test suite:
```powershell
pytest
```

---

## 💡 Useful Understanding Notes

### Architecture & File Role Clarifications: `app/main.py` vs. Package `__init__.py`

A common question when navigating this enterprise project structure is:
**"Why does `models` have `__init__.py`, and where does `main.py` belong (e.g., why not in `services/`)?"**

```text
my_enterprise_api/app/
├── __init__.py
├── main.py                     # <-- Application entry point
├── models/
│   └── __init__.py             # <-- SQLAlchemy ORM models package
├── schemas/
│   └── __init__.py             # <-- Pydantic validation schemas package
└── services/
    └── __init__.py             # <-- Business logic & CRUD layer package
```

#### 1. Why `models/`, `schemas/`, and `services/` use `__init__.py`
* In Python, an `__init__.py` file marks a directory as an importable Python package.
* Placing the module code or re-exports inside `__init__.py` provides clean, top-level package imports without cumbersome nested paths:
  - `from app.models import Product`
  - `from app.schemas import ProductCreate, ProductResponse`
  - `from app.services import BaseService`
* As the project scales, domain-specific files (e.g., `models/product.py`, `models/order.py`) can be introduced and re-exported through `__init__.py` without breaking existing imports across the application.

#### 2. Why `main.py` sits at the root of `app/`
* `app/main.py` is the **application entry point**, serving the entire application rather than any individual domain layer.
* Its core responsibilities include:
  - Initializing the central FastAPI application: `app = FastAPI(...)`
  - Managing application lifecycle events (`lifespan`) such as database connection pool startup and disposal
  - Configuring global middleware (e.g., CORS) and central exception handlers
  - Aggregating and mounting versioned API routers: `app.include_router(api_router)`
  - Acting as the entry target for ASGI web servers: `uvicorn app.main:app --reload`

#### 3. Layered Monolithic Architecture vs. Microservices
* **Microservices**: In a microservice ecosystem, each service runs as a separate, independently deployable server process with its own `main.py` entry point.
* **Clean Layered Monolith**: In this design, `services/` is merely an internal business logic layer (a package providing generic and specialized CRUD routines like `BaseService`), not an isolated server process. Thus, it only requires an `__init__.py`, while `app/main.py` drives the whole application.

---

### 🧩 Layer-by-Layer Package Breakdown (What Happens Where)

The application follows the **Separation of Concerns (SoC)** design principle. Here is what each layer and package handles:

| Layer / Package | Key Files | Primary Responsibility & What Is Happening |
| :--- | :--- | :--- |
| **Root Entry (`app/`)** | [`main.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/main.py) | **Application Assembly & Lifecycle:**<br>• Instantiates `FastAPI(lifespan=...)`.<br>• Uses the `lifespan` context manager to automatically create database tables on startup and cleanly dispose of engine pools on shutdown.<br>• Attaches global CORS middleware and exception handlers.<br>• Mounts all sub-routers with version prefixes (`/api/v1`). |
| **Core Infrastructure (`app/core/`)** | [`config.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/core/config.py)<br>[`database.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/core/database.py)<br>[`security.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/core/security.py) | **Environment, Connectivity & Security:**<br>• `config.py`: Reads environment variables (`.env`) into a typed Pydantic `Settings` class (DB credentials, API prefix, CORS rules).<br>• `database.py`: Configures the asynchronous SQLAlchemy connection pool (`create_async_engine`), creates the session factory (`async_sessionmaker`), and exposes `get_db()`, an async generator dependency injecting safe scoped DB sessions per request with automatic commit/rollback. |
| **Data Models (`app/models/`)** | [`__init__.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/models/__init__.py) | **Database Entity Schema (ORM):**<br>• Declares SQLAlchemy models (like `Product`) inheriting from `Base`.<br>• Defines the exact PostgreSQL table structure, columns, types (`UUID`, `JSONB`, `ARRAY`), unique constraints (`sku`), indexes, and default timestamp functions. |
| **Validation Schemas (`app/schemas/`)** | [`__init__.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/schemas/__init__.py) | **Data Transfer Objects (DTOs) & Validation:**<br>• Defines Pydantic schemas (`ProductBase`, `ProductCreate`, `ProductUpdate`, `ProductResponse`).<br>• Validates inbound request bodies (types, string lengths, positive numbers).<br>• Serializes outbound responses and controls field exposure (preventing internal DB fields from leaking). |
| **Services / Business Logic (`app/services/`)** | [`__init__.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/services/__init__.py) | **Business Logic & CRUD Abstraction:**<br>• Implements the generic `BaseService[ModelType, CreateSchemaType, UpdateSchemaType]`.<br>• Encapsulates asynchronous queries (`select`, `offset`, `limit`), model instantiation, and commit lifecycles (`get`, `get_multi`, `create`, `remove`).<br>• Decouples SQL/database logic from API endpoint handlers to make testing and maintenance easier. |
| **API Endpoints (`app/api/`)** | [`v1/api.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/api/v1/api.py)<br>[`v1/endpoints/products.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/api/v1/endpoints/products.py) | **Presentation & Routing (Controllers):**<br>• Routes incoming HTTP requests (`GET`, `POST`, `PUT`, `DELETE`).<br>• Parses query parameters (e.g. `skip`, `limit`, `search`, `tag`, `is_active`) and path parameters (`product_id`).<br>• Injects DB sessions via FastAPI dependency injection (`db: AsyncSession = Depends(get_db)`).<br>• Returns serialized responses and HTTP status codes (`200 OK`, `201 Created`, `204 No Content`, `404 Not Found`). |
| **Exceptions (`app/exceptions/`)** | [`__init__.py`](file:///d:/work/code/Ani-30-Days-Of-Python/29_Day_Building_API/python-fastapi-products-API/my_enterprise_api/app/exceptions/__init__.py) | **Error Handling & Normalization:**<br>• Defines custom exception classes (`AppException`, `NotFoundException`, `UnauthorizedException`).<br>• Registers FastAPI exception handlers (`setup_exception_handlers`) to intercept uncaught errors and format them into consistent JSON response structures (`{"success": false, "error": ...}`). |
| **Migrations (`migrations/`)** | Alembic configuration & versions | **Database Version Control:**<br>• Tracks schema evolution over time with Alembic revision scripts. |
| **Tests (`tests/`)** | Automated pytest suite | **Quality Assurance:**<br>• Async integration and unit tests verifying endpoints, response status codes, and database operations. |

