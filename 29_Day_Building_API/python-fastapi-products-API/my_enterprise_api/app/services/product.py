"""Product Service Layer (Domain Business Logic & Persistence).

📘 PYTHON & ARCHITECTURE LEARNER GUIDE:
Why does the `ProductService` class exist?
- It encapsulates all database access and domain rules for products.
- The route handlers in `app/api/v1/endpoints/products.py` simply delegate to this service.
- If we need to query products from an Orders API, an async task, or a test,
  we use `product_service` without repeating SQL queries.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.schemas import ProductCreate, ProductUpdate
from app.services import BaseService


# 📘 PYTHON GENERICS IN INHERITANCE:
# `BaseService` is a generic class defined as `Generic[ModelType, CreateSchemaType, UpdateSchemaType]`.
# Passing `[Product, ProductCreate, ProductUpdate]` in square brackets binds those three type placeholders:
# 1. ModelType        -> `Product`: Tells Python this service manages the SQLAlchemy `Product` database table.
# 2. CreateSchemaType -> `ProductCreate`: Specifies the Pydantic schema required when inserting a new product.
# 3. UpdateSchemaType -> `ProductUpdate`: Specifies the Pydantic schema used for partial/full updates.
#
# Benefits:
# - Reusability: Inherits standard CRUD methods (`get_multi()`, etc.) without rewriting SQL queries.
# - Type Safety & Autocomplete: Code editors know exact return types (e.g. `Product`, not generic `Any`).
class ProductService(BaseService[Product, ProductCreate, ProductUpdate]):
    """Domain service managing Product lifecycle, queries, and transactions."""

    async def get(self, db: AsyncSession, product_id: UUID) -> Optional[Product]:
        """Fetch a single product by its UUID primary key."""
        result = await db.execute(
            select(self.model).where(self.model.product_id == product_id)
        )
        return result.scalars().first()

    async def get_by_sku(self, db: AsyncSession, sku: str) -> Optional[Product]:
        """Fetch a single product by its unique business SKU."""
        result = await db.execute(
            select(self.model).where(self.model.sku == sku)
        )
        return result.scalars().first()

    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        tag: Optional[str] = None,
    ) -> List[Product]:
        """Retrieve paginated products with full-text search and filtering."""
        query = select(self.model)

        if is_active is not None:
            query = query.where(self.model.is_active == is_active)

        if search:
            search_filter = f"%{search}%"
            query = query.where(
                or_(
                    self.model.name.ilike(search_filter),
                    self.model.description.ilike(search_filter),
                    self.model.sku.ilike(search_filter),
                )
            )

        if tag:
            query = query.where(self.model.tags.any(tag))

        query = query.order_by(self.model.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: ProductCreate) -> Product:
        """Create a new product record from a Pydantic schema."""
        product_data = obj_in.model_dump()
        # Handle the PostgreSQL column alias mapping
        metadata_val = product_data.pop("metadata", {})

        db_obj = self.model(
            **product_data,
            metadata_info=metadata_val,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, *, db_obj: Product, obj_in: ProductUpdate
    ) -> Product:
        """Update fields on an existing product instance."""
        update_data = obj_in.model_dump(exclude_unset=True)

        if "metadata" in update_data:
            db_obj.metadata_info = update_data.pop("metadata")

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, product_id: UUID) -> Optional[Product]:
        """Find a product by UUID and remove it from the database."""
        product = await self.get(db, product_id=product_id)
        if product:
            await db.delete(product)
            await db.commit()
        return product


# Singleton instance ready for injection across endpoints
product_service = ProductService(Product)
