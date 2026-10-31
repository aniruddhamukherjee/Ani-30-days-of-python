"""Security & Cryptographic Utilities.

📘 PYTHON & SECURITY LEARNER GUIDE:
This module handles passwords and digital access tokens.

Key Security Concepts for Beginners:
1. One-Way Password Hashing:
   - NEVER store passwords as plaintext in a database! If a database is ever leaked,
     attackers would have everyone's real passwords.
   - Hashing is a one-way mathematical function:
     "password123" -> "$2b$12$e8uq...random_hash"
   - You can hash a password forward, but it is mathematically impossible to reverse the hash!
2. Password Verification:
   - When a user logs in, we hash their submitted password and compare it with the stored hash.
   - If the hashes match, they entered the right password!
3. JWT (JSON Web Tokens):
   - Think of a JWT like a digital VIP wristband at a concert.
   - Once a user logs in, the server stamps a token containing their user ID and expiration time.
   - The token is digitally signed with `settings.SECRET_KEY`.
   - On future requests, the client sends this token. The backend verifies the signature
     to confirm who the user is without querying the database for every single click!
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 📘 PASSWORD CONTEXT SETUP:
# `CryptContext` from Passlib manages password hashing algorithms.
# We choose "bcrypt", the industry standard for secure password hashing.
# `deprecated="auto"` ensures outdated hashing algorithms get upgraded automatically over time.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a user's typed password matches the stored bcrypt hash in the database.

    Args:
        plain_password (str): What the user typed into the login box (e.g., "secret123").
        hashed_password (str): The long scrambled hash stored in PostgreSQL.

    Returns:
        bool: True if password is correct, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Convert a plaintext password into an irreversible, salted bcrypt hash.

    Args:
        password (str): The new password to hash (e.g. on user registration).

    Returns:
        str: A secure salted hash string like "$2b$12$KIXu...".
    """
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a tamper-proof, digitally signed JSON Web Token (JWT).

    Args:
        subject (Union[str, Any]): The identity to store in the token (e.g. user_id or username).
        expires_delta (Optional[timedelta]): How long until this token expires.
            If None, uses our default duration from settings (7 days).

    Returns:
        str: Encrypted and signed JWT string.
    """
    # 📘 WORKING WITH TIMEZONES IN PYTHON 3.11+:
    # Always use timezone.utc! Using local server time causes bugs when servers change regions or daylight savings shifts.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # 📘 THE TOKEN PAYLOAD (CLAIMS):
    # 'exp': Expiration timestamp (standard JWT claim)
    # 'sub': Subject / owner of the token (standard JWT claim)
    to_encode = {"exp": expire, "sub": str(subject)}

    # Sign the dictionary with our secret key using the HS256 algorithm
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


