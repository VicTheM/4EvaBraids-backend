"""
Authenticate a user by username and password.
"""

from .get_user_by_email import get_user_by_email
from utils.crypt import verify_password
from models.user import UserOut


async def authenticate_user(username: str, password: str) -> UserOut:
    """
    Authenticate a user by username and password.

    Args:
    - username (str): The username of the user.
    - password (str): The password of the user.

    Returns:
    - UserOut: The user object if the user is authenticated, None otherwise.
    """
    user = await get_user_by_email(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
