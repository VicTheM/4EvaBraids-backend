"""
THIS FILES MODELS THE STATS OF THE SITE
"""
from pydantic import BaseModel


class ClickRequest(BaseModel):
    """
    This class models the request for the click endpoint
    
    Attributes:
        platform: either Whatsapp (W) or Instagram (G)
    """
    platform: str