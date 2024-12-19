from bson import ObjectId
from fastapi import APIRouter, HTTPException, status, Response
import service.user as user_service
from models import ObjectIdPydanticAnnotation
from models.user import UserCreate, UserOut
from typing import Annotated, List
from controllers import user as user_controller

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserOut:
    return await user_controller.create_user(user)


@router.get("", response_model=List[UserOut])
@router.get("/", response_model=List[UserOut])
async def get_all_users() -> List[UserOut]:
    return await user_controller.get_all_users()


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> UserOut:
    return await user_controller.get_user_by_id(user_id)


@router.get("/phone/{phone_number}", response_model=UserOut)
async def get_user_by_phone_number(phone_number: str) -> UserOut:
    await user_controller.get_user_by_phone_number(phone_number)


@router.get("/email/{email}", response_model=UserOut)
async def get_user_by_email(email: str) -> UserOut:
    await user_controller.get_user_by_email(email)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation], user: UserCreate
):
    user = await user_service.update_user(user_id, user)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
):
    user = await user_service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
