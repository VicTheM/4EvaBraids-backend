"""
Blog service module
"""

from typing import Annotated
from bson import ObjectId
from data.blog import BlogRepository
from exceptions import NotFound
from models import ObjectIdPydanticAnnotation
from models.blog import BlogInDB, BlogCreate, BlogOut, FullBlogOut
from controllers import user as user_controller
from fastapi import HTTPException, Depends, status

from models.user import UserOut

blog_repo = BlogRepository()
unauthorized = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not authorized to perform this action",
)


async def create_blog(blog: BlogCreate) -> BlogOut:
    """
    Create a new blog in the database

    Args:
        blog (BlogCreate): BlogCreate model

    Returns:
        BlogInDB: BlogInDB model
    """
    return FullBlogOut(**(await blog_repo.create_blog(blog)))


async def get_all_blogs() -> list[BlogOut]:
    """
    Get all blogs from the database

    Returns:
        list[BlogOut]: List of BlogOut models
    """
    return [BlogOut(**blog) for blog in await blog_repo.get_all_blogs()]


async def get_blog_by_id(
    blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> FullBlogOut:
    """
    Get a blog by id

    Args:
        blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): Blog id

    Returns:
        BlogInDB: BlogInDB model
    """
    blog = await blog_repo.get_blog_by_id(blog_id)
    if blog:
        return FullBlogOut(**blog)
    raise NotFound(detail="Blog not found")


async def update_blog(
    blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
    blog: BlogCreate,
    user: UserOut,
) -> FullBlogOut:
    """
    Update a blog

    Args:
        blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): Blog id
        blog (BlogCreate): BlogCreate model

    Returns:
        BlogInDB: BlogInDB model
    """
    blog_in_db = await blog_repo.get_blog_by_id(blog_id)
    if not blog_in_db:
        raise NotFound(detail="Blog not found")
    if blog_in_db["user_id"] != user.id:
        raise unauthorized
    updated_blog = await blog_repo.update_blog(blog_id, blog)
    return FullBlogOut(**updated_blog)


async def delete_blog(
    blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation], user: UserOut
) -> bool:
    """
    Delete a blog

    Args:
        blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): Blog id

    Returns:
        bool: True if deleted
    """
    blog_in_db = await blog_repo.get_blog_by_id(blog_id)
    if not blog_in_db:
        raise NotFound(detail="Blog not found")
    if blog_in_db["user_id"] != user.id:
        raise unauthorized
    deleted_blog = await blog_repo.delete_blog(blog_id)
    return deleted_blog
