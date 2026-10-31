"""Pydantic Validation & Data Transfer Object (DTO) Schemas.

📘 PYTHON & PYDANTIC LEARNER GUIDE:
Why do we have "models" AND "schemas"? Isn't that redundant?
NO! This is one of the most important enterprise architecture patterns:
1. SQLAlchemy Models (`app/models/`):
   - Blueprints for the **Database** (tables, columns, primary keys, SQL types).
2. Pydantic Schemas (`app/schemas/`):
   - Blueprints for **Network Communication** (incoming JSON from users, outgoing JSON to clients).

Key Python Concepts in This File:
1. Data Validation:
   - If a client sends `"price": -50`, Pydantic intercepts it with `gt=0` and returns:
     "422 Unprocessable Entity: Price must be greater than 0" before your code even runs!
2. The Ellipsis (`...`) in `Field(...)`:
   - In Python, `...` is a built-in singleton called `Ellipsis`.
   - In Pydantic, `Field(...)` means: "This field is REQUIRED! Do not allow None or missing."
3. Why `default_factory=list` instead of `default=[]`?
   - In Python, lists and dictionaries are mutable.
   - If you write `default=[]`, EVERY product instance would share the exact same list in memory!
   - `default_factory=list` tells Python: "Call list() to create a brand new empty list every time."
4. Class Inheritance (`class ProductCreate(ProductBase): pass`):
   - DRY (Don't Repeat Yourself): `ProductCreate` inherits all fields from `ProductBase` for free!
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


# 📘 BASE SCHEMA (Common attributes shared across create, read, and response)
class ProductBase(BaseModel):
    """Base product attributes common to all representations."""

    # `...` means REQUIRED. `max_length=50` limits text length.
    sku: str = Field(..., max_length=50, description="Unique product SKU")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Detailed product description")
    
    # `gt=0` ensures prices can never be zero or negative
    price: float = Field(..., gt=0, description="Product price (must be positive)")
    
    # `ge=0` ensures stock count cannot be negative numbers
    stock_quantity: int = Field(default=0, ge=0, description="Available stock quantity")
    
    # 📘 WHAT IS AliasChoices?
    # In PostgreSQL/SQLAlchemy, the column is mapped to Python attribute `metadata_info`.
    # But in frontend JSON, users expect the field named "metadata".
    # `AliasChoices` allows Pydantic to seamlessly accept either name!
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        validation_alias=AliasChoices("metadata_info", "metadata"),
        serialization_alias="metadata",
        description="Arbitrary product metadata in JSON format",
    )
    
    # `default_factory=list` ensures each product gets its own separate list
    tags: List[str] = Field(
        default_factory=list, description="Array of product tags"
    )
    is_active: bool = Field(default=True, description="Whether product is active")


# 📘 CREATE SCHEMA:
# When a client sends POST /api/v1/products, we validate against this schema.
# Notice `pass`: it has the exact same fields as ProductBase, no duplicate code needed!
class ProductCreate(ProductBase):
    """Schema for validating product creation requests (POST /api/v1/products)."""
    pass


# 📘 UPDATE SCHEMA:
# When updating an item (PUT /api/v1/products/{id}), users might only want to change the price.
# Therefore, every single field here is `Optional[...] = None`.
class ProductUpdate(BaseModel):
    """Schema for updating an existing product (supports partial updates)."""

    sku: Optional[str] = Field(None, max_length=50, description="Updated unique SKU")
    name: Optional[str] = Field(None, description="Updated product name")
    description: Optional[str] = Field(None, description="Updated product description")
    price: Optional[float] = Field(None, gt=0, description="Updated unit price (must be positive)")
    stock_quantity: Optional[int] = Field(None, ge=0, description="Updated inventory count (>= 0)")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        validation_alias=AliasChoices("metadata_info", "metadata"),
        serialization_alias="metadata",
        description="Updated metadata JSON object",
    )
    tags: Optional[List[str]] = Field(None, description="Updated list of categorization tags")
    is_active: Optional[bool] = Field(None, description="Updated active status flag")


# 📘 RESPONSE SCHEMA:
# When sending data back to the user, we include database-generated read-only fields:
# `product_id`, `created_at`, and `updated_at`.
class ProductResponse(ProductBase):
    """Schema for serializing products returned to API clients."""

    product_id: UUID
    created_at: datetime
    updated_at: datetime

    # 📘 WHAT IS ConfigDict(from_attributes=True)?
    # By default, Pydantic only knows how to read Python dictionaries: `dict["name"]`.
    # SQLAlchemy queries return ORM objects: `product.name`.
    # `from_attributes=True` tells Pydantic: "If input is an object with attributes, read those too!"
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


