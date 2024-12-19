"""
This module contains the controller for fetching a user by their email address.
"""

from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserOut
from exceptions import NotFound


async def get_user_by_email(email: str) -> UserOut:
    """
    Fetch a user by their email address.

    Args:
        email (str): The email address of the user to fetch.

    Returns:
        UserOut: The user information if found.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTP exception with the appropriate message.
    """
    try:
        user = await user_service.get_user_by_email(email)
        return user
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
