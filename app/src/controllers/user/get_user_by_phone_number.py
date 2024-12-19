"""
This module contains the controller for retrieving a user by their phone number.
"""

from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserOut
from exceptions import NotFound


async def get_user_by_phone_number(phone_number: str) -> UserOut:
    """
    Retrieve a user by their phone number.

    Args:
        phone_number (str): The phone number of the user to retrieve.

    Returns:
        UserOut: The user information if found.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTP exception with the appropriate message.
    """
    try:
        user = await user_service.get_user_by_phone_number(phone_number)
        return user
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
