from models import ObjectIdPydanticAnnotation, ExcludedField
from models.comment import CommentInDB
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import datetime as dt
from bson import ObjectId
from typing import Annotated


class BlogCreate(BaseModel):
    user_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(
        ..., alias="user_id"
    )
    thumbnail: str = Field(..., min_length=2, max_length=100)
    title: str = Field(..., min_length=2, max_length=50)
    body: str = Field(..., min_length=2, max_length=10000)

    model_config = ConfigDict(from_attributes=True)


class BlogInDB(BlogCreate):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(
        default_factory=ObjectId, alias="_id"
    )
    preview: str = Field(..., min_length=2, max_length=100)
    likes: int = Field(default=0)
    comments: list[CommentInDB] = Field(default_factory=list)
    date_created: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )
    date_updated: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc)
    )



class BlogOut(BlogInDB):
    body: ExcludedField[str | None] = None


class FullBlogOut(BlogInDB):
    pass
