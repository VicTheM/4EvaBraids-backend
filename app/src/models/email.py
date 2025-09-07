from pydantic import BaseModel, EmailStr
from config import settings
from typing import List

class EmailemailSettings(BaseModel):
    """
    This class Holds configuration for sending emails
    """
    MAIL_USERNAME: str = settings.EMAIL
    MAIL_PASSWORD: str = settings.PASSWORD
    MAIL_FROM: EmailStr = settings.EMAIL
    MAIL_FROM_NAME: str = "4evabraids"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False      # This might have to chnage to True when we deploy
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False
    RECEIVERS_EMAIL: List[EmailStr] = ["victorychibuike111@gmail.com"]