"""Automated Test Suite for Application Endpoints.

📘 PYTHON LEARNER GUIDE: How Automated Testing Works:
Instead of opening Postman or your browser and manually clicking around every time you change
a line of code, we write automated test scripts!

Key Python & Testing Concepts in This File:
1. What is `pytest`?
   - The most popular testing framework in Python.
   - When you run `pytest` in your terminal, it automatically searches for files named `test_*.py`,
     executes every function starting with `def test_*()`, and reports passing/failing tests.
2. The `@pytest.mark.asyncio` Decorator:
   - Our FastAPI route handlers are asynchronous (`async def`).
   - Standard Python functions can't `await` things. This marker tells pytest:
     "Run this test inside an asyncio event loop so we can test async code!"
3. Lightning Fast In-Memory Testing (`ASGITransport`):
   - Normally, to test an API you have to start Uvicorn, wait for a port, send a real network request, and shut down.
   - `httpx.ASGITransport(app=app)` bypasses the network entirely!
   - It sends HTTP requests directly into our Python FastAPI object in memory.
   - Tests run in milliseconds without port conflicts!
4. Python `assert` Statements:
   - `assert response.status_code == 200`
   - If the statement is True, Python silently continues.
   - If the statement is False, Python stops immediately and highlights the exact line that failed!
"""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


# 📘 TEST FUNCTION:
# Pytest discovers any function whose name begins with `test_`.
@pytest.mark.asyncio
async def test_health_check() -> None:
    """Test the `/health` endpoint to ensure the application starts and is healthy."""

    # 1. Create an asynchronous test client hooked directly to our FastAPI app
    # `async with` ensures the test client is opened and closed cleanly
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        
        # 2. Send an asynchronous GET request to /health
        response = await client.get("/health")
        
        # 3. Verify the HTTP response status code is 200 OK
        assert response.status_code == 200
        
        # 4. Parse the JSON response body into a Python dictionary
        data = response.json()
        
        # 5. Verify the dictionary has the expected values
        assert data["status"] == "healthy"
        assert "Enterprise Products API" in data["project"]


