"""Global Exception Handling & Error Normalization.

📘 PYTHON LEARNER GUIDE: How Exceptions & Error Handlers Work:
In Python, when something goes wrong (e.g. division by zero or a file doesn't exist),
Python "raises an exception" and halts execution.

Key Python & API Concepts Demonstrated Here:
1. Custom Exception Classes & Inheritance:
   - Python lets you create your own error types!
   - `class AppException(Exception)` means `AppException` is a child of Python's built-in `Exception`.
   - `class NotFoundException(AppException)` is a grandchild. It automatically has status 404!
2. The `super()` Function:
   - `super().__init__(message)` calls the constructor of the parent class, passing the
     error message up to Python's internal exception system.
3. FastAPI Centralized Exception Handlers (`@app.exception_handler`):
   - Without this, if an unexpected error happens in Python, users see an ugly crash page or raw traceback.
   - Centralized handlers "catch" the error like a safety net and return a neat, predictable JSON payload:
     {
         "success": false,
         "error": "Product with ID '...' not found.",
         "status_code": 404
     }
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


# 📘 BASE APPLICATION EXCEPTION:
# Inherits from Python's built-in `Exception`.
# All custom errors in our app inherit from this base class.
class AppException(Exception):
    """Base error class for our application.

    Holds both an error message and the HTTP status code (default: 400 Bad Request).
    """

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        # Pass the message to Python's built-in Exception class
        super().__init__(self.message)


# 📘 SPECIFIC ERROR CLASSES (INHERITANCE):
# Instead of remembering status numbers, developers can write:
#     raise NotFoundException("Item not found")
class NotFoundException(AppException):
    """Raised when something isn't found in the database (HTTP 404 Not Found)."""

    def __init__(self, message: str = "Resource not found"):
        # Calls AppException.__init__ with status 404
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    """Raised when a user is not logged in or has an invalid token (HTTP 401 Unauthorized)."""

    def __init__(self, message: str = "Unauthorized"):
        # Calls AppException.__init__ with status 401
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


# 📘 ATTACHING HANDLERS TO FASTAPI:
def setup_exception_handlers(app: FastAPI) -> None:
    """Connect error handlers to the FastAPI app instance."""

    # 1. Catch all known AppException errors (400, 401, 404, etc.)
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        """Translates custom python exceptions into structured JSON responses."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.message,
                "status_code": exc.status_code,
            },
        )

    # 2. Safety Net: Catch ANY unexpected crash or unhandled bug in Python (HTTP 500)
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catches unexpected bugs, preventing sensitive server tracebacks from leaking to users."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "An unexpected internal server error occurred.",
                "status_code": 500,
            },
        )


