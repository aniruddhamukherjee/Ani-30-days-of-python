"""Core Application Package.

📘 PYTHON LEARNER TIP: What is __init__.py?
In Python, putting a file named `__init__.py` inside a folder tells Python:
"Treat this entire folder as an importable package!"
Because of this file, other Python scripts can write:
    from app.core.config import settings
    from app.models import Product

This file runs automatically as soon as the `app` package is imported anywhere in our project.

🏗️ Project Architecture Overview:
- `core/`: Fundamental infrastructure (settings, database connection, security helpers).
- `models/`: Database blueprints (SQLAlchemy classes that mirror SQL tables).
- `schemas/`: Input/output blueprints (Pydantic models that check and clean data).
- `services/`: The "chef in the kitchen" (business logic doing database queries).
- `api/`: The "waiters" (FastAPI route endpoints receiving HTTP requests from clients).
- `exceptions/`: Custom error definitions and global error formatters.
- `main.py`: The application starting point that ties everything together.
"""

