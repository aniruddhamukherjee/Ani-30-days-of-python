"""Business Logic & Generic CRUD Service Layer.

📘 PYTHON & ARCHITECTURE LEARNER GUIDE:
Why does the `services/` layer exist?
In a small demo app, people often write raw database queries directly inside route handlers.
In professional enterprise software, this becomes a mess:
- If 5 different endpoints need to fetch a product, you'd write the same query 5 times.
- If you change how products are saved, you'd have to edit 5 different files!

The Solution: The Service / Repository Layer!
`BaseService` is a reusable "helper" that handles the 4 fundamental database operations (CRUD):
- C: Create (POST)
- R: Read   (GET)
- U: Update (PUT)
- D: Delete (DELETE)

Advanced Python Concepts in This File:
1. Python Generics & `TypeVar`:
   - Notice `Generic[ModelType, CreateSchemaType, UpdateSchemaType]`.
   - `TypeVar` is a placeholder (like variable `x` in algebra).
   - If we pass `Product`, Python knows this service returns `Product` objects.
   - If tomorrow we build `UserService`, we can inherit from `BaseService` without rewriting any CRUD code!
2. Dictionary Unpacking (`**kwargs`):
   - `db_obj = self.model(**obj_in_data)`
   - The double asterisk `**` unpacks a dictionary like `{"name": "Shoes", "price": 50}` into
     keyword arguments: `Product(name="Shoes", price=50)`.
3. SQLAlchemy 2.0 Query Execution:
   - `await db.execute(select(...))`: Sends the query asynchronously to PostgreSQL.
   - `.scalars()`: Unwraps rows from raw tuples into pure Python model objects.
   - `.first()`: Returns the first object found, or `None` if no match exists.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base

# 📘 WHAT ARE TYPEVARS?
# They act as typed placeholders so your code editor (VS Code, IDE) gives you accurate autocomplete.
ModelType = TypeVar("ModelType", bound=Base)               # Represents any SQLAlchemy model
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # Represents any Pydantic Create schema
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # Represents any Pydantic Update schema


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic asynchronous CRUD service providing reusable database operations.

    Args:
        model: The SQLAlchemy model class (e.g. Product) this service instance operates on.
    """

    def __init__(self, model: Type[ModelType]):
        # Store the model class (e.g. Product) so we can query and instantiate it
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Fetch a single record by its primary key ID (returns None if not found)."""
        # 📘 SQL GENERATED: SELECT * FROM <table> WHERE id = :id LIMIT 1;
        result = await db.execute(select(self.model).where(self.model.id == id))
        # `.scalars().first()` extracts the Python object from the database result
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Fetch multiple paginated records using offset and limit."""
        # 📘 SQL GENERATED: SELECT * FROM <table> OFFSET :skip LIMIT :limit;
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        # `.all()` returns all matching records as a Python list
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Convert a Pydantic schema into an ORM model and save it to the database."""
        # 1. Turn the Pydantic schema into a standard Python dictionary
        obj_in_data = obj_in.model_dump()
        
        # 2. Unpack the dictionary into the model class using `**`
        # Equivalent to: Product(sku="...", name="...", price=...)
        db_obj = self.model(**obj_in_data)
        
        # 3. Add the object to the session (staged for insertion)
        db.add(db_obj)
        
        # 4. Commit: Sends the SQL INSERT statement to PostgreSQL
        await db.commit()
        
        # 5. Refresh: Reloads the object so Python has the database-generated ID & timestamps
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """Find a record by its ID and delete it from the database."""
        # 1. Check if the record actually exists first
        obj = await self.get(db, id=id)
        if obj:
            # 2. Stage the object for deletion
            await db.delete(obj)
            # 3. Send the SQL DELETE statement to PostgreSQL
            await db.commit()
        return obj


