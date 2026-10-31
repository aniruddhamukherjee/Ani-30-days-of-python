"""SQLAlchemy Database Models (ORM Entity Layer).

📘 PYTHON & SQLALCHEMY LEARNER GUIDE:
This file defines the shape of our data in PostgreSQL.

Key Python & Database Concepts Explained:
1. What is an ORM Model?
   - In Python, `class Product(Base):` is a class.
   - But in PostgreSQL, it becomes a real database table named `products`!
   - Every column defined with `Column(...)` maps directly to a column in SQL.
2. Passing Functions as Defaults (Look closely: `default=uuid.uuid4`, no parentheses!):
   - If we wrote `default=uuid.uuid4()`, Python would run the function once when the app starts
     and assign that single UUID to every product forever!
   - By omitting the parentheses, we pass the function itself. SQLAlchemy calls it freshly
     every time a new row is inserted.
3. Python `lambda` Functions:
   - `lambda: datetime.now(timezone.utc)` is a one-line anonymous function.
   - It runs at the exact millisecond a record is saved, stamping the current time.
4. Float vs. Numeric for Money:
   - Python floats (e.g., `0.1 + 0.2 = 0.30000000000000004`) have binary rounding errors.
   - In enterprise apps, prices must ALWAYS use `Numeric(10, 2)` (fixed-point decimal).
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID

from app.core.database import Base


class Product(Base):
    """The Product model representing the 'products' table in PostgreSQL."""

    # 📘 SQL TABLE NAME:
    # Tells SQLAlchemy: "Create or look for a table named 'products' in Postgres"
    __tablename__ = "products"

    # 📘 PRIMARY KEY (UUIDv4):
    # Instead of sequential auto-incrementing numbers (1, 2, 3...) which are easy for
    # competitors to guess, we use a 128-bit globally unique identifier (UUID).
    # `as_uuid=True` tells Python to treat this as a native Python `uuid.UUID` object.
    product_id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    # 📘 STOCK KEEPING UNIT (SKU):
    # A short code like "TECH-AUD-001".
    # `unique=True`: PostgreSQL will reject inserts if the SKU already exists.
    # `index=True`: Creates a B-Tree database index for lightning-fast search lookups.
    sku = Column(String(50), unique=True, nullable=False, index=True)

    # 📘 TEXT ATTRIBUTES:
    # `nullable=False`: Required field. Database will error if someone tries to save NULL.
    # `nullable=True`: Optional field. It's okay if left empty.
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    # 📘 FINANCIAL / INVENTORY ATTRIBUTES:
    # `Numeric(10, 2)`: Up to 10 total digits, 2 digits after the decimal point (e.g. 99999999.99).
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)

    # 📘 ADVANCED POSTGRESQL SPECIFIC DATA TYPES:
    # 1. JSONB (Binary JSON):
    #    Allows storing arbitrary nested dictionary data like {"color": "black", "bluetooth": "5.3"}.
    #    The column in PostgreSQL is named "metadata", mapped to attribute `metadata_info` in Python.
    metadata_info = Column("metadata", JSONB, nullable=True, default=dict)
    
    # 2. ARRAY(Text):
    #    PostgreSQL natively supports storing lists/arrays of strings like ['audio', 'wireless'].
    tags = Column(ARRAY(Text), nullable=True, default=list)

    # 📘 BOOLEAN STATUS:
    # Flag to hide/show products without deleting them from the database ("soft status").
    is_active = Column(Boolean, nullable=False, default=True)

    # 📘 AUDIT TIMESTAMPS:
    # `created_at`: Set once when the row is first created.
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    # `updated_at`: `onupdate` tells SQLAlchemy to update this timestamp whenever the row is modified.
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


