from models.user import UserOut
from web.auth import oauth2_scheme
import jwt
from fastapi import HTTPException, Depends, status
from config import settings
from controllers import user as user_controller


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    """
    Get the current user from the access token.

    Args:
        token (str): The access token.

    Returns:
        dict: The user data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await user_controller.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
