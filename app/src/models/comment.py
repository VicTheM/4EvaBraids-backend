from typing import Annotated
from bson import ObjectId
from models import ObjectIdPydanticAnnotation
from pydantic import BaseModel, Field
from datetime import datetime
import datetime as dt


class CommentCreate(BaseModel):
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(
        ..., alias="user_id"
    )
    text: str = Field(..., min_length=2, max_length=1000)


class CommentInDB(CommentCreate):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(
        default_factory=ObjectId, alias="_id"
    )
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )

    class Config:
        from_attributes = True


class CommentOut(CommentInDB):
    class Config:
        from_attributes = True

    pass
