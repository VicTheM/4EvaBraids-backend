"""
Update an existing user.
"""

from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserCreate, UserOut
from exceptions import AlreadyExists, NotFound


async def update_user(user_id: str, user: UserCreate) -> UserOut:
    """
    Update an existing user.

    Args:
        user_id (str): The ID of the user to update.
        user (UserCreate): The user data to update.

    Returns:
        UserOut: The updated user data.

    Raises:
        HTTPException: If the user is not found (404) or if the user already exists (400).
    """
    try:
        user = await user_service.update_user(user_id, user)
        return user
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        )
