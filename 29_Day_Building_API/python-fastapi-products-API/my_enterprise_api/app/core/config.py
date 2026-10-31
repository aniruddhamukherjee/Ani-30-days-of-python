"""Global Configuration Management.

📘 PYTHON LEARNER GUIDE: How Application Settings Work:
Instead of hardcoding database passwords, secret keys, and server URLs across multiple files,
we centralize all settings in this single module using `pydantic-settings`.

Key Python Concepts Demonstrated Here:
1. `BaseSettings`: A special Pydantic class that automatically checks:
   - "Is there an environment variable set on the computer/Docker with this name?"
   - "If not, is there a `.env` text file containing it?"
   - "If not, fallback to the default value provided here in Python!"
2. Type Hinting (e.g. `POSTGRES_PORT: int = 5432`):
   - Tells Python and Pydantic what type each setting must be. If someone sets
     POSTGRES_PORT="abc", Pydantic will raise a helpful validation error on startup!
3. `@property` Decorator:
   - Turns a function into a calculated "getter" attribute so you can write
     `settings.ASYNC_DATABASE_URL` instead of `settings.ASYNC_DATABASE_URL()`.
"""

from typing import List, Union
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration class for the entire backend application."""

    # 📘 PROJECT IDENTITY & ROUTING
    PROJECT_NAME: str = "Enterprise Products API"
    API_V1_STR: str = "/api/v1"

    # 📘 SECURITY & TOKENS
    # SECRET_KEY: A secret random string used to sign JSON Web Tokens (JWT).
    # In production, this should always be overridden in your `.env` file!
    SECRET_KEY: str = "super-secret-key-change-this-in-production-min-32-chars"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days (60 min * 24 hrs * 7 days)
    ALGORITHM: str = "HS256"

    # 📘 CORS (Cross-Origin Resource Sharing)
    # List of frontend URLs permitted to send API requests to this backend.
    # `Union[str, AnyHttpUrl]` means each item can be either a regular string or a validated URL object.
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = [
        "http://localhost:3000",  # Common default port for React / Next.js
        "http://localhost:8000",  # Local API docs and Swagger UI
    ]

    # 📘 POSTGRESQL DATABASE CREDENTIALS
    # These match the database server we connect to.
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"

    # 📘 WHAT IS A PYTHON @property?
    # By placing `@property` above this method, we can access it like a normal variable:
    # `settings.ASYNC_DATABASE_URL` (no parentheses needed).
    # It dynamically constructs the database connection string using our variables.
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Dynamically assemble the PostgreSQL connection URI for the asyncpg driver.

        Format:
            postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
        """
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # 📘 PYDANTIC SETTINGS BEHAVIOR CONFIGURATION:
    model_config = SettingsConfigDict(
        # Read from a file named `.env` in the project root if it exists
        env_file=".env",
        env_file_encoding="utf-8",
        # Case sensitive: POSTGRES_PORT matches POSTGRES_PORT, not postgres_port
        case_sensitive=True,
        # If there are extra variables in the .env file, don't crash, just ignore them
        extra="ignore",
    )


# 📘 CREATE A SINGLETON INSTANCE:
# We instantiate `Settings()` once here.
# Any other file in our project simply does: `from app.core.config import settings`
settings = Settings()


