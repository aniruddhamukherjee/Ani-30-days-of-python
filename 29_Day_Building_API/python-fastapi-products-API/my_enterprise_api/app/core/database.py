"""Database Infrastructure & Asynchronous Session Management.

📘 PYTHON & SQLALCHEMY LEARNER GUIDE:
This module connects Python to our PostgreSQL database.

Key Python & Database Concepts Explained:
1. ORM (Object-Relational Mapping):
   - Without an ORM, you have to write raw SQL strings like `SELECT * FROM products;`.
   - With SQLAlchemy ORM, database tables become Python classes (`Product`), and table rows
     become Python objects (`product = Product(name="Shoes", price=99.99)`).
2. Asynchronous I/O (`async` / `await`):
   - Talking to a database requires sending data over a network cable and waiting for a reply.
   - Using `async/await` with `asyncpg` means Python DOES NOT sit frozen waiting for the database;
     it immediately serves other users while waiting!
3. Connection Pooling:
   - Creating a brand new database connection for every single click is slow and heavy.
   - A "pool" keeps a handful (e.g. 10) of ready-to-use connections open in memory.
   - When a request comes in, it "borrows" a connection, runs the query, and returns it to the pool.
4. Python Generators (`yield`):
   - `get_db()` is a generator function. It prepares a database session, "yields" it to the
     request handler to run SQL, and when the handler finishes, Python resumes right after
     the `yield` to commit or rollback the transaction and close the session!
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# 📘 CREATING THE ASYNC ENGINE:
# The engine is the central source of database connections.
# - pool_pre_ping=True: Tests the connection before giving it to you (prevents "server disconnected" crashes).
# - pool_size=10: Keeps 10 ready-to-use connections in the pool at all times.
# - max_overflow=20: If 30 people visit at the exact same millisecond, allows 20 temporary extra connections.
# - future=True: Enables modern SQLAlchemy 2.0 syntax.
engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    echo=False,  # Set to True if you want SQLAlchemy to print every raw SQL query to your console
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# 📘 SESSION FACTORY:
# A "session" is like an open conversation with the database where you can add, query,
# or delete objects before saving them with `commit()`.
# `async_sessionmaker` creates a factory that stamps out fresh `AsyncSession` objects.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,       # You must explicitly say `session.commit()` to save changes
    autoflush=False,        # Don't send partial SQL to the DB until we are ready
    expire_on_commit=False, # Keeps Python object attributes readable even after saving
    class_=AsyncSession,
)

# 📘 DECLARATIVE BASE CLASS:
# All our database models in `app/models/` will inherit from this `Base` class.
# It tracks all registered models so SQLAlchemy knows how to create the database tables.
Base = declarative_base()


# 📘 DEPENDENCY INJECTION GENERATOR FUNCTION:
# In FastAPI endpoints, you will see: `db: AsyncSession = Depends(get_db)`.
# FastAPI calls `get_db()`, grabs the yielded `session`, hands it to your route function,
# and guarantees that cleanup code (commit/rollback/close) runs when the request is done!
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a scoped asynchronous database session for each incoming HTTP request."""
    # 1. Open a fresh database session from our connection pool
    async with AsyncSessionLocal() as session:
        try:
            # 2. Yield the session to the FastAPI route handler to perform queries
            yield session
            # 3. If everything succeeded without errors, permanently save changes to the database
            await session.commit()
        except Exception:
            # 4. If any error occurred during the request, cancel/undo all pending changes
            await session.rollback()
            # Re-raise the exception so error handlers can catch and report it
            raise
        finally:
            # 5. Guaranteed cleanup: close the session and return the connection to the pool
            await session.close()


