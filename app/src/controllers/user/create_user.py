"""
This module contains the controller for creating a new user.
"""

from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserCreate, UserOut
from exceptions import AlreadyExists


async def create_user(user: UserCreate) -> UserOut:
    """
    Asynchronously creates a new user.

    Args:
        user (UserCreate): The user data required to create a new user.

    Returns:
        UserOut: The created user data.

    Raises:
        HTTPException: If the user already exists, raises an HTTP 400 Bad Request error with a relevant message.
    """
    try:
        user = await user_service.create_user(user)
        return user
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
