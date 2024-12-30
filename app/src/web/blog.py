"""
Blog Routes
"""

from bson import ObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from models import ObjectIdPydanticAnnotation
from controllers import user as user_controller
from models.blog import BlogCreate, BlogInDB, BlogOut, FullBlogOut
from typing import Annotated, List
from service import blog as blog_service
from web.auth import oauth2_scheme

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post(
    "/", response_model=FullBlogOut, status_code=status.HTTP_201_CREATED
)
async def create_blog(
    blog: BlogCreate, user=Depends(user_controller.get_current_user)
) -> FullBlogOut:
    """
    Create a new blog.

    Args:
        blog (BlogCreate): The blog data required to create a new blog.

    Returns:
        FullBlogOut: The created blog data.
    """
    blog.user_id = user.id
    return await blog_service.create_blog(blog)


@router.get("/", response_model=List[BlogOut])
async def get_all_blogs() -> List[BlogOut]:
    """
    Retrieve all blogs.

    Returns:
        List[BlogOut]: A list of blog data.
    """
    return await blog_service.get_all_blogs()


@router.get("/{blog_id}", response_model=FullBlogOut)
async def get_blog_by_id(
    blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation]
) -> FullBlogOut:
    """
    Retrieve a blog by its ID.

    Args:
        blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The blog ID.

    Returns:
        FullBlogOut: The blog data.
    """
    return await blog_service.get_blog_by_id(blog_id)


@router.put("/{blog_id}", response_model=FullBlogOut)
async def update_blog(
    blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
    blog: BlogCreate,
    user=Depends(user_controller.get_current_user),
) -> FullBlogOut:
    """
    Update a blog by its ID.

    Args:
        blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The blog ID.
        blog (BlogCreate): The blog data to update.

    Returns:
        FullBlogOut: The updated blog data.
    """
    return await blog_service.update_blog(blog_id, blog, user)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: Annotated[ObjectId, ObjectIdPydanticAnnotation],
    user=Depends(user_controller.get_current_user),
) -> Response:
    """
    Delete a blog by its ID.

    Args:
        blog_id (Annotated[ObjectId, ObjectIdPydanticAnnotation]): The blog ID.

    Returns:
        Response: The response.
    """
    await blog_service.delete_blog(blog_id, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
