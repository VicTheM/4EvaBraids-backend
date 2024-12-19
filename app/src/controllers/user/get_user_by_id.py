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
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=e.message
        )
