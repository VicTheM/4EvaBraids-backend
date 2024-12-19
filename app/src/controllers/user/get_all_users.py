"""
This module contains the controller for fetching all users.
"""

from models.user import UserOut
from service import user as user_service


async def get_all_users() -> list[UserOut]:
    """
    Fetches all users from the user service.

    Returns:
        list[UserOut]: A list of user objects.
    """
    users = await user_service.get_all_users()
    return users
