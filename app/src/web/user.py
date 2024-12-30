"""
User routes.
"""

from bson import ObjectId
from fastapi import APIRouter, status, Depends
from models import ObjectIdPydanticAnnotation
from models.user import UserCreate, UserOut
from typing import Annotated, List
from controllers import user as user_controller
from .auth import oauth2_scheme

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
async def get_current_user(
    user: UserOut = Depends(user_controller.get_current_user),
) -> UserOut:
    """
    Get the current user.

    Args:
        user (UserOut): The current user.

    Returns:
        UserOut: The current user data.
    """
    return user


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserOut:
    """
    Create a new user.

    Args:
        user (UserCreate): The user data required to create a new user.

    Returns:
        UserOut: The created user data.
    """
    return await user_controller.create_user(user)


@router.get("/", response_model=List[UserOut])
async def get_all_users(token: str = Depends(oauth2_scheme)) -> List[UserOut]:
    """
    Retrieve all users.

    Returns:
        List[UserOut]: A list of user data.
    """
    return await user_controller.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
    user: UserOut = Depends(user_controller.get_current_user),
) -> UserOut:
    """
    Retrieve a user by their ID.

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The ID of the user to retrieve.

    Returns:
        UserOut: The user data if found.
    """
    return await user_controller.get_user_by_id(user_id)


@router.get("/phone/{phone_number}", response_model=UserOut)
async def get_user_by_phone_number(
    phone_number: str,
    user: UserOut = Depends(user_controller.get_current_user),
) -> UserOut:
    """
    Retrieve a user by their phone number.

    Args:
        phone_number (str): The phone number of the user to retrieve.

    Returns:
        UserOut: The user information if found.
    """
    await user_controller.get_user_by_phone_number(phone_number)


@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(
    email: str, user: UserOut = Depends(user_controller.get_current_user)
) -> UserOut:
    """
    Retrieve a user by their email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        UserOut: The user information if found.
    """
    await user_controller.get_user_by_email(email)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
    user_update: UserCreate,
    user: UserOut = Depends(user_controller.get_current_user),
) -> UserOut:
    """
    Update a user.

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The ID of the user to update.
        user (UserCreate): The updated user data.

    Returns:
        UserOut: The updated user data.
    """
    return await user_controller.update_user(user_id, user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
    user: UserOut = Depends(user_controller.get_current_user),
) -> None:
    """
    Delete a user.

    Args:
        user_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The ID of the user to delete.
    """
    return await user_controller.delete_user(user_id)
