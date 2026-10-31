"""API Version 1 Router Aggregator.

📘 PYTHON & FASTAPI LEARNER GUIDE:
Think of `APIRouter` like folders in your computer's file system:
- Instead of having 50 different endpoints scattered around, we create sub-routers.
- This file acts as the master junction for Version 1 of our API (`/api/v1`).

How Path Prefixing Works (URL Math):
1. `main.py` mounts this router with prefix: `/api/v1`
2. This file mounts `products.router` with prefix: `/products`
3. In `products.py`, an endpoint defines: `GET /`
-> Final URL: `/api/v1` + `/products` + `/` = `/api/v1/products/`
"""

from fastapi import APIRouter
from app.api.v1.endpoints import products

# 📘 CREATE THE V1 ROUTER:
# This router will collect all feature routers under version 1
api_router = APIRouter()

# 📘 REGISTER FEATURE ROUTERS:
# - `prefix="/products"`: Prepends '/products' to every endpoint inside products.router.
# - `tags=["Products"]`: Tells Swagger UI (interactive docs) to group all these endpoints
#   under a neat, collapsible "Products" heading!
api_router.include_router(products.router, prefix="/products", tags=["Products"])


