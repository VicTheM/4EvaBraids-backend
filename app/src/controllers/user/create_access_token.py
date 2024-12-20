"""
This module contains the logic to create an access token for a user.
"""

import jwt
from datetime import datetime, timedelta
from config import settings
import datetime as dt


async def create_access_token(user_id: int) -> str:
    """
    Create an access token for a user.

    Args:
    - user_id (int): The ID of the user.

    Returns:
    - str: The access token.
    """
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now(dt.UTC)
        + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
    }
    return jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
