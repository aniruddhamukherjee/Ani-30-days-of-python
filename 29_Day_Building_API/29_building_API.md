<div align="center">
  <h1> 30 Days Of Python: Day 29 - Building an API with FastAPI, PostgreSQL & Docker </h1>
</div>

[<< Day 28](../28_Day_API/28_API.md) | [Day 30 >>](../30_Day_Conclusions/30_conclusions.md)

![30DaysOfPython](../images/30DaysOfPython_banner3@2x.png)

- [Day 29: Building APIs](#day-29-building-apis)
  - [Introduction to RESTful APIs](#introduction-to-restful-apis)
  - [Why FastAPI? Modern Python vs Traditional Frameworks](#why-fastapi-modern-python-vs-traditional-frameworks)
- [Enterprise Project Architecture](#enterprise-project-architecture)
- [Database Setup: PostgreSQL with Advanced Types](#database-setup-postgresql-with-advanced-types)
- [Building the Application Layer by Layer](#building-the-application-layer-by-layer)
  - [1. Environment Configuration (Pydantic BaseSettings)](#1-environment-configuration-pydantic-basesettings)
  - [2. Asynchronous Database Connection (SQLAlchemy 2.0 & asyncpg)](#2-asynchronous-database-connection-sqlalchemy-20--asyncpg)
  - [3. Database Models (SQLAlchemy ORM)](#3-database-models-sqlalchemy-orm)
  - [4. Data Validation Schemas (Pydantic v2)](#4-data-validation-schemas-pydantic-v2)
  - [5. API Routing & Endpoints (CRUD)](#5-api-routing--endpoints-crud)
  - [6. Global Exception Handling](#6-global-exception-handling)
  - [7. Main Application Entry Point & Lifespan](#7-main-application-entry-point--lifespan)
- [Containerization & Orchestration](#containerization--orchestration)
  - [Multi-Stage Dockerfile](#multi-stage-dockerfile)
  - [Docker Compose Orchestration](#docker-compose-orchestration)
- [Testing & API Exploration](#testing--api-exploration)
  - [Interactive Swagger & ReDoc Docs](#interactive-swagger--redoc-docs)
  - [Testing with Postman](#testing-with-postman)
  - [Automated Testing with Pytest](#automated-testing-with-pytest)
- [💻 Exercises: Day 29](#-exercises-day-29)

---

## Day 29: Building APIs

### Introduction to RESTful APIs

A **RESTful API** (Representational State Transfer) is an architectural style for providing networked systems with a standardized interface to manipulate data using standard **HTTP methods**:

| HTTP Method | Purpose | Typical SQL/CRUD Equivalent | Idempotent |
| :--- | :--- | :--- | :---: |
| `GET` | Retrieve resource(s) | `SELECT` (Read) | Yes |
| `POST` | Create a new resource | `INSERT` (Create) | No |
| `PUT` | Full update or replace resource | `UPDATE` (Update) | Yes |
| `PATCH` | Partial update of resource | `UPDATE` (Partial) | No |
| `DELETE` | Remove a resource | `DELETE` (Delete) | Yes |

---

### Why FastAPI? Modern Python vs Traditional Frameworks

For years, Python developers built APIs using frameworks like Flask or Django. However, modern high-scale backend services demand:
1. **Asynchronous I/O (`async`/`await`)**: Enables handling tens of thousands of concurrent database queries and network calls on a single instance without blocking execution threads.
2. **Type Safety & Automatic Validation**: Python 3 type hints paired with [Pydantic](https://docs.pydantic.dev/) eliminate manual JSON parsing, type conversions, and input sanitation.
3. **Automatic OpenAPI (Swagger) Documentation**: Complete interactive documentation is automatically generated from your Python code, zero manual documentation maintenance required.

| Feature | Flask (Legacy) | FastAPI (Modern Standard) |
| :--- | :--- | :--- |
| **Concurrency Model** | Synchronous WSGI | Asynchronous ASGI (`asyncio`) |
| **Performance** | Moderate | Extremely high (comparable to Go & NodeJS) |
| **Request Validation** | Manual boilerplate | Automatic via Pydantic type annotations |
| **API Documentation** | Requires third-party plugins | Native OpenAPI 3.1 & Swagger UI |
| **Dependency Injection** | Basic extensions | First-class, type-safe `Depends()` system |

---

## Enterprise Project Architecture

In professional production environments, backend applications adhere to **Clean Layered Architecture**, separating concerns across configuration, database models, schemas, and routes:

```text
my_enterprise_api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # App initialization, CORS & lifespan
│   ├── core/                       # Global configs & database engine
│   │   ├── config.py               # Pydantic BaseSettings (.env support)
│   │   ├── database.py             # Async DB session lifecycle (asyncpg)
│   │   └── security.py             # Security utilities
│   ├── exceptions/                 # Global error handling
│   │   └── __init__.py
│   ├── api/                        # API version routing
│   │   └── v1/
│   │       ├── api.py              # Router aggregator
│   │       └── endpoints/
│   │           └── products.py     # Product CRUD endpoints
│   ├── models/                     # SQLAlchemy ORM Database Models
│   │   └── __init__.py
│   ├── schemas/                    # Pydantic Request/Response Validation
│   │   └── __init__.py
│   └── services/                   # Business Logic Layer
│       └── __init__.py
├── migrations/                     # Alembic database migrations
├── tests/                          # Automated Pytest suite
│   └── test_main.py
├── .env                            # Environment variables
├── Dockerfile                      # Multi-stage production container
├── docker-compose.yml              # Local multi-service orchestration
└── requirements.txt                # Project dependencies
```

---

## Database Setup: PostgreSQL with Advanced Types

Our API manages a **`products`** catalog backed by PostgreSQL, utilizing advanced relational features:
- **`UUID`**: Cryptographically secure, globally unique primary keys.
- **`JSONB`**: Binary JSON for storing schema-less product attributes (specifications, dimensions, custom attributes).
- **`text[]` (Array)**: Native array storage for product tags and categories.
- **`timestamptz`**: Timezone-aware creation and update timestamps.

```sql
CREATE TABLE products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb,
    tags TEXT[] DEFAULT ARRAY[]::text[],
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()
);
```

---

## Building the Application Layer by Layer

### 1. Environment Configuration (Pydantic BaseSettings)

We manage environment variables securely using `pydantic-settings`. Values can be overridden per environment (`.env`, staging, production):

```python
# app/core/config.py
from typing import List, Union
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Products API"
    API_V1_STR: str = "/api/v1"

    # CORS
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
```

---

### 2. Asynchronous Database Connection (SQLAlchemy 2.0 & asyncpg)

Instead of traditional blocking database drivers, we use `asyncpg` with an async connection pool:

```python
# app/core/database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Create async engine with connection pooling
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection yielding an async session per request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

### 3. Database Models (SQLAlchemy ORM)

Map the relational `products` table into Python classes:

```python
# app/models/__init__.py
from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, Numeric, String, Text, Integer
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    metadata_info = Column("metadata", JSONB, nullable=True, default=dict)
    tags = Column(ARRAY(Text), nullable=True, default=list)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
```

---

### 4. Data Validation Schemas (Pydantic v2)

Pydantic schemas enforce incoming request payload structures, types, and validate business rules (e.g., price must be greater than zero):

```python
# app/schemas/__init__.py
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    sku: str = Field(..., max_length=50, description="Unique product SKU")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Detailed product description")
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    stock_quantity: int = Field(default=0, ge=0, description="Available stock quantity")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        validation_alias=AliasChoices("metadata", "metadata_info"),
        description="Arbitrary product metadata in JSON format",
    )
    tags: List[str] = Field(default_factory=list, description="Array of product tags")
    is_active: bool = Field(default=True, description="Whether product is active")


class ProductCreate(ProductBase):
    """Schema used when creating a new product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product (all fields optional)."""
    sku: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    metadata: Optional[Dict[str, Any]] = Field(
        None, validation_alias=AliasChoices("metadata", "metadata_info")
    )
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema returned to API clients."""
    product_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
```

---

### 5. API Routing & Endpoints (CRUD)

Define the CRUD endpoints using FastAPI's `APIRouter`:

```python
# app/api/v1/endpoints/products.py
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


# 1. READ ALL (with filtering & pagination)
@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    tag: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Product)
    if is_active is not None:
        query = query.where(Product.is_active == is_active)
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            or_(
                Product.name.ilike(search_filter),
                Product.description.ilike(search_filter),
                Product.sku.ilike(search_filter),
            )
        )
    if tag:
        query = query.where(Product.tags.any(tag))

    query = query.order_by(Product.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


# 2. READ ONE BY ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product


# 3. CREATE
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Product).where(Product.sku == product_in.sku))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="SKU already exists.")

    product_data = product_in.model_dump()
    metadata_val = product_data.pop("metadata", {})
    product = Product(**product_data, metadata_info=metadata_val)
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# 4. UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    update_data = product_in.model_dump(exclude_unset=True)
    if "metadata" in update_data:
        product.metadata_info = update_data.pop("metadata")

    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)
    return product


# 5. DELETE
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    await db.delete(product)
    await db.commit()
    return None
```

---

### 6. Global Exception Handling

Ensure API responses always maintain a predictable JSON contract even during unhandled failures:

```python
# app/exceptions/__init__.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message, "status_code": exc.status_code},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "An unexpected internal server error occurred.",
                "status_code": 500,
            },
        )
```

---

### 7. Main Application Entry Point & Lifespan

Connect middleware, exception handlers, routers, and application lifespans:

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.exceptions import setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: clean up DB pool
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

setup_exception_handlers(app)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}
```

---

## Containerization & Orchestration

### Multi-Stage Dockerfile

A production Dockerfile uses **multi-stage compilation** to keep the final container image minimal, fast, and secure:

```dockerfile
# Stage 1: Build & Compile wheels
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Minimal runtime image
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled dependencies only
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

---

### Docker Compose Orchestration

Run your PostgreSQL database and the FastAPI application seamlessly together using `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: enterprise_fastapi_app
    restart: always
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - POSTGRES_SERVER=db
    volumes:
      - ./app:/app/app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:latest
    container_name: enterprise_postgres_db
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

Start the entire environment with:
```powershell
docker compose up --build -d
```

---

## Testing & API Exploration

### Interactive Swagger & ReDoc Docs

Once the app is running, visit:
- **Swagger UI**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **ReDoc**: [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)

From Swagger UI, click **"Try it out"** on any endpoint to send live queries directly from your browser.

---

### Testing with Postman

#### Option 1: One-Click Collection Import
1. In Postman, click **Import** (top-left).
2. Enter the OpenAPI raw URL: `http://localhost:8000/api/v1/openapi.json`.
3. Postman automatically builds the complete collection with all endpoints, schema definitions, and paths.

#### Option 2: Making Sample Requests

**Create Product (`POST /api/v1/products/`)**:
```json
{
  "sku": "TECH-AUD-001",
  "name": "Wireless Noise-Cancelling Headphones",
  "description": "High-fidelity sound with 40-hour battery life",
  "price": 199.99,
  "stock_quantity": 40,
  "metadata": {
    "brand": "SonicWave",
    "color": "Matte Black",
    "bluetooth": "5.3"
  },
  "tags": ["audio", "wireless", "electronics"],
  "is_active": true
}
```

**List Products with Filter (`GET /api/v1/products/?search=Headphones&is_active=true`)**:
Returns an array of matching products ordered by creation date.

---

### Automated Testing with Pytest

Run automated tests using `httpx` async client:

```python
# tests/test_main.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
```

Execute tests with:
```powershell
pytest
```

---

## 💻 Exercises: Day 29

1. **Deploy Locally**: Start the PostgreSQL container and run the API using Uvicorn (`uvicorn app.main:app --reload`).
2. **Execute Full CRUD**: Use Postman to perform a complete lifecycle: Create a product, Retrieve it by SKU, Update its price, and Delete it.
3. **Extend Query Filtering**: Add price range filters (`min_price` and `max_price`) to the `list_products` endpoint in `app/api/v1/endpoints/products.py`.
4. **Containerize**: Build the Docker image using `docker compose up --build` and verify the API responds on `http://localhost:8000/health`.

🎉 CONGRATULATIONS ON COMPLETING DAY 29! 🎉

[<< Day 28](../28_Day_API/28_API.md) | [Day 30 >>](../30_Day_Conclusions/30_conclusions.md)
