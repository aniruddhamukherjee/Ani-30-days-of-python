"""Product Catalog REST API Endpoints.

📘 PYTHON & FASTAPI LEARNER GUIDE:
This file contains the "Route Handlers" (often called "Controllers" in other frameworks).
Each function here corresponds to an incoming HTTP request from a web browser, mobile app, or client.

Key Architecture & Framework Concepts in This File:
1. Is Database Initialized Here? (`db: AsyncSession = Depends(get_db)`):
   - NO! Database tables and engine connection pools are NOT initialized here.
     Initialization happens ONCE on application startup inside `lifespan` in `app/main.py`.
   - `Depends(get_db)` is FastAPI's request-scoped Dependency Injection:
     1. Borrows one ready-to-use database session from the connection pool (`AsyncSessionLocal`).
     2. Hands the session to this route function as `db`.
     3. When the endpoint finishes, `get_db` automatically runs its `finally` block to commit,
        rollback on error, and return the connection cleanly to the pool.
2. Why Can't `product_service` Keep a Single Global `db`?
   - In async servers, hundreds of requests run concurrently at the exact same millisecond.
   - If a global `self.db` was shared across all requests, one user's query or rollback would
     corrupt another user's database transaction!
   - Per-request sessions ensure strict transaction isolation and thread-safe concurrency.
3. Service Layer Delegation (`product_service`):
   - Controllers handle HTTP concerns: status codes, path/query parsing, and DTO serialization.
   - Business rules, domain validation, and SQL queries are delegated to `product_service`.
4. HTTP Methods & Conventions:
   - GET    -> Retrieve data (idempotent, safe, no database changes).
   - POST   -> Create a new item (returns 201 Created).
   - PUT    -> Replace/update an existing item (modifies database).
   - DELETE -> Remove an item (returns 204 No Content with empty body).
5. Path Parameters vs. Query Parameters (`Query(...)`):
   - Path parameter (`/{product_id}`): Identifies a specific resource in the URL hierarchy.
   - Query parameter (`?skip=10&limit=20`): Modifies or filters requests (pagination, search).
   - `Query(...)`: Declares defaults, OpenAPI/Swagger descriptions, and validation rules
     (e.g., `ge=0`, `le=100`) so malformed client queries fail early with 422 Unprocessable Entity.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service

# 📘 CREATE THE PRODUCTS SUB-ROUTER:
router = APIRouter()


# ---------------------------------------------------------------------------
# 1. LIST PRODUCTS (GET /api/v1/products/)
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[ProductResponse])
async def list_products(
    # 📘 WHAT IS FASTAPI Query()?
    # `Query(...)` declares that this value is parsed from the URL query string (e.g. `?skip=10&limit=20`).
    # Beyond marking the parameter, it provides three powerful enterprise features:
    # 1. Default Value: `Query(0)` sets the fallback if the client omits `?skip=...`.
    # 2. Input Validation Constraints:
    #    - `ge=0` ("greater than or equal to 0"): Rejects negative offsets like `?skip=-5`.
    #    - `le=100` ("less than or equal to 100"): Prevents clients from requesting millions of rows.
    #    - If validation fails, FastAPI automatically halts execution and returns a 422 error!
    # 3. Interactive Documentation: `description="..."` renders directly in Swagger UI (`/docs`).
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of items to return"),
    search: Optional[str] = Query(None, description="Search term matching product name, description, or SKU"),
    is_active: Optional[bool] = Query(None, description="Filter products by active status (true/false)"),
    tag: Optional[str] = Query(None, description="Filter products that contain this tag in their PostgreSQL text array"),
    db: AsyncSession = Depends(get_db),
) -> List[Product]:
    """Retrieve a paginated, filterable list of products.

    Inputs:
        - skip (int, query): Number of records to skip for pagination (default: 0, ge: 0).
        - limit (int, query): Maximum number of records to return (default: 50, 1-100).
        - search (str, optional, query): Case-insensitive match on name, description, or SKU.
        - is_active (bool, optional, query): Filter by active status (true/false).
        - tag (str, optional, query): Match tag in PostgreSQL text array.
        - db (AsyncSession, dependency): Request-scoped database session injected via Depends(get_db).

    Outputs:
        - 200 OK: List of products serialized according to `ProductResponse` schema.
    """
    return await product_service.get_multi_filtered(
        db,
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
        tag=tag,
    )


# ---------------------------------------------------------------------------
# 2. GET PRODUCT BY UUID (GET /api/v1/products/{product_id})
# ---------------------------------------------------------------------------
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID, db: AsyncSession = Depends(get_db)
) -> Product:
    """Retrieve a single product by its UUID primary key.

    Inputs:
        - product_id (UUID, path): Unique 128-bit UUID identifier of the product.
        - db (AsyncSession, dependency): Request-scoped database session injected via Depends(get_db).

    Outputs:
        - 200 OK: Single `ProductResponse` object matching the UUID.
        - 404 NOT FOUND: Raised if no product with the specified UUID exists.
    """
    product = await product_service.get(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' not found.",
        )
    return product


# ---------------------------------------------------------------------------
# 3. GET PRODUCT BY SKU (GET /api/v1/products/sku/{sku})
# ---------------------------------------------------------------------------
@router.get("/sku/{sku}", response_model=ProductResponse)
async def get_product_by_sku(
    sku: str, db: AsyncSession = Depends(get_db)
) -> Product:
    """Retrieve a single product by its unique business SKU.

    Inputs:
        - sku (str, path): Unique business Stock Keeping Unit (e.g. "TECH-AUD-001").
        - db (AsyncSession, dependency): Request-scoped database session injected via Depends(get_db).

    Outputs:
        - 200 OK: Single `ProductResponse` object matching the unique SKU.
        - 404 NOT FOUND: Raised if no product with the specified SKU exists.
    """
    product = await product_service.get_by_sku(db, sku=sku)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU '{sku}' not found.",
        )
    return product


# ---------------------------------------------------------------------------
# 4. CREATE PRODUCT (POST /api/v1/products/)
# ---------------------------------------------------------------------------
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate, db: AsyncSession = Depends(get_db)
) -> Product:
    """Validate and insert a brand new product record.

    Inputs:
        - product_in (ProductCreate, body): Validated JSON payload containing product attributes
          (sku, name, price > 0, stock_quantity >= 0, metadata, tags).
        - db (AsyncSession, dependency): Request-scoped database session injected via Depends(get_db).

    Outputs:
        - 201 CREATED: Successfully created product serialized as `ProductResponse`.
        - 400 BAD REQUEST: Raised if a product with the provided SKU already exists.
        - 422 UNPROCESSABLE ENTITY: Auto-raised by Pydantic if incoming JSON violates schema.
    """
    # Check if a product with this SKU already exists
    existing = await product_service.get_by_sku(db, sku=product_in.sku)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product_in.sku}' already exists.",
        )
    return await product_service.create(db, obj_in=product_in)


# ---------------------------------------------------------------------------
# 5. UPDATE PRODUCT (PUT /api/v1/products/{product_id})
# ---------------------------------------------------------------------------
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)
) -> Product:
    """Update fields on an existing product (supports partial updates).

    Inputs:
        - product_id (UUID, path): Target product UUID to update.
        - product_in (ProductUpdate, body): Partial update JSON with optional fields
          (e.g., only updating price or stock).
        - db (AsyncSession, dependency): Request-scoped database session injected via Depends(get_db).

    Outputs:
        - 200 OK: Updated product serialized as `ProductResponse`.
        - 404 NOT FOUND: Raised if target product_id does not exist.
        - 422 UNPROCESSABLE ENTITY: Auto-raised by Pydantic if input fields fail validation.
    """
    product = await product_service.get(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' not found.",
        )
    return await product_service.update(db, db_obj=product, obj_in=product_in)


# ---------------------------------------------------------------------------
# 6. DELETE PRODUCT (DELETE /api/v1/products/{product_id})
# ---------------------------------------------------------------------------
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID, db: AsyncSession = Depends(get_db)
) -> None:
    """Permanently delete a product record by its UUID.

    Inputs:
        - product_id (UUID, path): Target product UUID to delete.
        - db (AsyncSession, dependency): Request-scoped database session injected via Depends(get_db).

    Outputs:
        - 204 NO CONTENT: Successfully deleted with empty response body.
        - 404 NOT FOUND: Raised if target product_id does not exist.
    """
    product = await product_service.remove(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' not found.",
        )
    return None


