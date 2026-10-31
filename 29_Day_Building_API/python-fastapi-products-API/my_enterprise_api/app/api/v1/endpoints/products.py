"""Product Catalog REST API Endpoints.

📘 PYTHON & FASTAPI LEARNER GUIDE:
This file contains the "Route Handlers" (often called "Controllers" in other frameworks).
Each function here corresponds to an HTTP request from a web browser, mobile app, or Postman.

Key Python & FastAPI Concepts in This File:
1. HTTP Methods:
   - GET    -> Retrieve data (does not modify database).
   - POST   -> Create a new item (returns 201 Created).
   - PUT    -> Update an existing item (modifies database).
   - DELETE -> Remove an item (returns 204 No Content).
2. Path Parameters vs. Query Parameters:
   - Path parameter: `@router.get("/{product_id}")` -> Part of the URL: `/products/123`
   - Query parameter: `skip: int = Query(0)` -> Passed after a question mark: `/products?skip=10&limit=20`
3. Dependency Injection (`Depends(get_db)`):
   - You don't have to manually connect and disconnect the database inside every function!
   - FastAPI automatically runs `get_db()`, hands the database session to `db`, and cleans it up when done.
4. Dynamic SQL Query Construction with SQLAlchemy:
   - Notice how we start with `query = select(Product)` and conditionally append `.where(...)`.
   - Python lets us build complex SQL queries piece-by-piece cleanly using Python logic!
5. Built-in `setattr()` Function:
   - `setattr(object, "price", 99.99)` is Python's way of doing `object.price = 99.99` dynamically from a loop!
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Product
from app.schemas import ProductCreate, ProductResponse, ProductUpdate

# 📘 CREATE THE PRODUCTS SUB-ROUTER:
router = APIRouter()


# ---------------------------------------------------------------------------
# 1. LIST PRODUCTS (GET /api/v1/products/)
# ---------------------------------------------------------------------------
@router.get("/", response_model=List[ProductResponse])
async def list_products(
    # 📘 FASTAPI Query() PARAMETERS:
    # `ge=0` means "greater than or equal to 0" (prevents negative offsets)
    # `le=100` means "less than or equal to 100" (protects the database from huge requests)
    skip: int = Query(0, ge=0, description="Number of items to skip for pagination"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of items to return"),
    search: Optional[str] = Query(None, description="Search term matching product name, description, or SKU"),
    is_active: Optional[bool] = Query(None, description="Filter products by active status (true/false)"),
    tag: Optional[str] = Query(None, description="Filter products that contain this tag in their PostgreSQL text array"),
    # 📘 INJECT DATABASE SESSION:
    db: AsyncSession = Depends(get_db),
) -> List[Product]:
    """Retrieve a paginated, filterable list of products."""
    
    # Start building our SQL query: SELECT * FROM products
    query = select(Product)

    # 📘 CONDITIONAL FILTERING:
    # Notice: we check `is not None` because `is_active` could be `False` (which is falsy in Python!)
    if is_active is not None:
        query = query.where(Product.is_active == is_active)

    # Full text search across name, description, and SKU
    # `.ilike` is PostgreSQL's case-insensitive LIKE operator (e.g. "phone" matches "iPhone")
    if search:
        search_filter = f"%{search}%"
        # `or_()` groups conditions: WHERE (name LIKE ... OR description LIKE ... OR sku LIKE ...)
        query = query.where(
            or_(
                Product.name.ilike(search_filter),
                Product.description.ilike(search_filter),
                Product.sku.ilike(search_filter),
            )
        )

    # PostgreSQL native array check: checks if `tag` exists anywhere inside `tags TEXT[]`
    if tag:
        query = query.where(Product.tags.any(tag))

    # Order by newest first, and apply pagination offset and limit
    query = query.order_by(Product.created_at.desc()).offset(skip).limit(limit)
    
    # Execute query asynchronously over the connection
    result = await db.execute(query)
    
    # `.scalars().all()` extracts all matching Python Product objects as a list
    return list(result.scalars().all())


# ---------------------------------------------------------------------------
# 2. GET PRODUCT BY UUID (GET /api/v1/products/{product_id})
# ---------------------------------------------------------------------------
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID, db: AsyncSession = Depends(get_db)
) -> Product:
    """Retrieve a single product by its UUID primary key."""
    # Run SQL: SELECT * FROM products WHERE product_id = :product_id LIMIT 1;
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    product = result.scalars().first()
    
    # If no product was found with this ID, raise an HTTP 404 Not Found error
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
    """Retrieve a single product by its unique business SKU."""
    result = await db.execute(select(Product).where(Product.sku == sku))
    product = result.scalars().first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU '{sku}' not found.",
        )
    return product


# ---------------------------------------------------------------------------
# 4. CREATE PRODUCT (POST /api/v1/products/)
# ---------------------------------------------------------------------------
# `status_code=201`: Standard HTTP status for "Successfully Created"
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    # FastAPI automatically validates incoming request JSON against ProductCreate schema!
    product_in: ProductCreate, db: AsyncSession = Depends(get_db)
) -> Product:
    """Validate and insert a brand new product record."""
    
    # 📘 PREVENT DUPLICATES (Validation before DB insert):
    # Check if a product with this SKU already exists to avoid a raw PostgreSQL IntegrityError crash
    existing = await db.execute(select(Product).where(Product.sku == product_in.sku))
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product_in.sku}' already exists.",
        )

    # 📘 DICTIONARY CONVERSION & POP:
    # 1. Turn the validated Pydantic model into a dictionary
    product_data = product_in.model_dump()
    
    # 2. Extract "metadata" and remove it from the dict using `pop()`
    # We do this because the Python model column is named `metadata_info`
    metadata_val = product_data.pop("metadata", {})

    # 3. Instantiate the SQLAlchemy Product model using dictionary unpacking (`**`)
    product = Product(
        **product_data,
        metadata_info=metadata_val,
    )
    
    # 4. Stage, commit, and refresh the new record
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


# ---------------------------------------------------------------------------
# 5. UPDATE PRODUCT (PUT /api/v1/products/{product_id})
# ---------------------------------------------------------------------------
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID, product_in: ProductUpdate, db: AsyncSession = Depends(get_db)
) -> Product:
    """Update fields on an existing product (supports partial updates)."""
    
    # 1. Find the target product
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' not found.",
        )

    # 📘 WHAT IS exclude_unset=True?
    # If the user only sent `{"price": 19.99}`, we don't want all the other fields
    # (name, description, etc.) to be overwritten with None!
    # `exclude_unset=True` ensures dictionary ONLY contains fields the user actually sent.
    update_data = product_in.model_dump(exclude_unset=True)

    # Handle the metadata alias mapping if present
    if "metadata" in update_data:
        product.metadata_info = update_data.pop("metadata")

    # 📘 DYNAMIC ATTRIBUTE UPDATE USING setattr():
    # Instead of writing `if "price" in update_data: product.price = update_data["price"]`
    # for 10 different fields, Python's built-in `setattr(obj, key, val)` updates them in a clean loop!
    for field, value in update_data.items():
        setattr(product, field, value)

    # Save changes to the database
    await db.commit()
    await db.refresh(product)
    return product


# ---------------------------------------------------------------------------
# 6. DELETE PRODUCT (DELETE /api/v1/products/{product_id})
# ---------------------------------------------------------------------------
# `status_code=204`: Standard HTTP status for "No Content" (successful delete with empty response body)
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: UUID, db: AsyncSession = Depends(get_db)
) -> None:
    """Permanently delete a product record by its UUID."""
    result = await db.execute(select(Product).where(Product.product_id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' not found.",
        )

    # Stage deletion and execute SQL DELETE
    await db.delete(product)
    await db.commit()
    return None


