"""
Contains the logic to retrieve a user by their ID.
"""

from typing import Annotated
from bson import ObjectId
from fastapi import HTTPException, status
from models import ObjectIdPydanticAnnotation
from service import user as user_service
from models.user import UserOut
from exceptions import NotFound


async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserOut:
    """
    Retrieve a user by their ID.

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The ID of the user to retrieve.

    Returns:
        UserOut: The user data if found.

    Raises:
        HTTPException: If the user is not found, raises a 404 HTTP exception with the appropriate message.
    """
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
