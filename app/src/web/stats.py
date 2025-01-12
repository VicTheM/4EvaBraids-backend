"""
This file defines the route used to record app stats
"""
from fastapi import APIRouter
from models.stats import ClickRequest
from service.stats import register_socials_click
from service.stats import get_clicks

router = APIRouter(prefix="/stats", tags=["stats"])


@router.post("/register_click")
async def register_social_click(socials: ClickRequest):
    """
    ClickRequest is either "W" or "G"
    Register a click on the site.
    """
    print(f"click: {socials}")
    await register_socials_click(socials)
    return {"message": "Click registered successfully"}


@router.get("/clicks")
async def fetch_clicks():
    """
    Get the number of clicks on the site
    """
    return await get_clicks()