from datetime import datetime
import datetime as dt
from typing import Annotated

from bson import ObjectId
from models import ObjectIdPydanticAnnotation, ExcludedField
from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(
        ..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    phone_number: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6, max_length=50)

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserCreate):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(
        default_factory=ObjectId, alias="_id"
    )
    hashed_password: str = Field(..., min_length=6, max_length=80)
    password: ExcludedField[str | None] = None
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )


class UserOut(UserInDB):
    hashed_password: ExcludedField[str | None] = None

    pass
