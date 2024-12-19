"""
This module contains the controller for deleting a user.
"""

from fastapi import HTTPException, status
from service import user as user_service
from exceptions import NotFound


async def delete_user(user_id: str):
    """
    Asynchronously deletes a user by their user ID.

    Args:
        user_id (str): The ID of the user to be deleted.

    Raises:
        HTTPException: If the user is not found, raises an HTTP 404 Not Found exception.
    """
    try:
        await user_service.delete_user(user_id)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
