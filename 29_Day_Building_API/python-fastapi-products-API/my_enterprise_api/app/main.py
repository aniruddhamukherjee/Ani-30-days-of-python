"""Application Entry Point.

📘 PYTHON & FASTAPI LEARNER GUIDE:
This is the starting file of our entire web application.
When you run a command like:
    uvicorn app.main:app --reload

It means:
- "Look inside the `app` folder"
- "Open the `main.py` file"
- "Find the variable named `app` (which is our FastAPI instance) and start running it!"
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.exceptions import setup_exception_handlers


# 📘 WHAT IS AN ASYNC CONTEXT MANAGER & LIFESPAN?
# In modern FastAPI, `lifespan` replaces older `@app.on_event("startup")` events.
# Think of it like opening and closing a shop:
# 1. Everything BEFORE the `yield` statement runs once when the app STARTS UP (opening shop).
# 2. The `yield` pauses this function and lets the app run and answer client requests.
# 3. Everything AFTER the `yield` runs once when the app SHUTS DOWN (closing shop).
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown events cleanly."""
    
    # --- STARTUP (Before yield) ---
    # `async with` is a Python context manager for asynchronous code.
    # It safely acquires a database connection, performs tasks, and releases it.
    print("🚀 [Startup] Application is starting up...")
    async with engine.begin() as conn:
        # `run_sync` runs synchronous SQLAlchemy functions (like create_all) inside async code.
        # This checks the database and creates the SQL tables if they don't exist yet!
        await conn.run_sync(Base.metadata.create_all)
    print("✅ [Startup] Database tables verified/created.")
    
    # The application now runs and accepts HTTP requests here!
    yield
    
    # --- SHUTDOWN (After yield) ---
    # When you press Ctrl+C to stop the server, code continues here.
    print("🛑 [Shutdown] Application is shutting down...")
    # `dispose()` cleanly closes all pooled database connections so nothing leaks.
    await engine.dispose()
    print("👋 [Shutdown] Database connections closed.")


# 📘 CREATING THE FASTAPI APPLICATION OBJECT:
# `app` is the main engine of our project.
# We configure its title, where interactive Swagger docs (`docs_url`) and OpenAPI specs live,
# and link the `lifespan` manager we defined above.
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# 📘 WHAT IS CORS (Cross-Origin Resource Sharing)?
# By default, web browsers block a frontend (e.g. React running on http://localhost:3000)
# from making API requests to a backend on a different port (e.g. http://localhost:8000).
# CORS middleware tells the browser: "It is safe to allow requests from these trusted origins!"
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # Allow requests from origins listed in our settings (e.g., React/Vue frontends)
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        # Allow cookies and authentication headers to be sent
        allow_credentials=True,
        # Allow all standard HTTP methods: GET, POST, PUT, DELETE, OPTIONS, etc.
        allow_methods=["*"],
        # Allow all standard headers (Authorization, Content-Type, etc.)
        allow_headers=["*"],
    )

# 📘 GLOBAL EXCEPTION HANDLERS:
# Connect our centralized error handling function so unhandled errors return clean JSON
# instead of an ugly Python traceback crash page.
setup_exception_handlers(app)

# 📘 MOUNTING ROUTERS:
# Instead of cramming all endpoints into this one file, we split them into modules (routers).
# `include_router` plugs those modular endpoints into our main application under `/api/v1`.
app.include_router(api_router, prefix=settings.API_V1_STR)


# 📘 WHAT IS A ROUTE DECORATOR?
# The `@app.get(...)` syntax is a Python "Decorator".
# It tells FastAPI: "Whenever someone sends an HTTP GET request to `/health`,
# run this `health_check()` function and return the result as JSON."
@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint.

    Useful for monitoring tools (like Docker or Kubernetes) to ask:
    "Is this service healthy and alive?"
    """
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "api_version": settings.API_V1_STR,
    }


