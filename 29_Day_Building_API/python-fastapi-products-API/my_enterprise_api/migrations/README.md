# Database Migrations (Alembic)

This directory is configured for database migrations using Alembic.

### Common Commands:
1. Initialize/generate new migration:
   ```bash
   alembic revision --autogenerate -m "Add new migration"
   ```
2. Apply all pending migrations:
   ```bash
   alembic upgrade head
   ```
3. Roll back last migration:
   ```bash
   alembic downgrade -1
   ```
