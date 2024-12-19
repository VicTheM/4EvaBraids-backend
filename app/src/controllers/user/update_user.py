from fastapi import HTTPException, status
from service import user as user_service
from models.user import UserCreate, UserOut
from exceptions import AlreadyExists, NotFound


async def update_user(user_id: str, user: UserCreate) -> UserOut:
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
