"""
This file defines the route used to book an appointment
"""
from fastapi import APIRouter
from fastapi import BackgroundTasks
from utils.send_mail import send_email
from web.auth import oauth2_scheme
from fastapi import HTTPException, Depends, status
from controllers import user as user_controller
import jwt
from config import settings

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/")
async def create_appointment(background_tasks: BackgroundTasks, location: str = "unknown",
                             style: str = "Unknown", date: str = "01-01-2025", time: str = "00.00am",
                             token: str = Depends(oauth2_scheme)):
    """
    Create an appointment. Get redirected for authentication if not loggedin
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await user_controller.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    # Build up the message to be sent
    subject = "You have a new appointment"
    content = f'''
    Hello, you have a booking with the following details:
    
    Name:   {user.first_name} {user.last_name}
    Phone:  {user.phone_number}
    Email:  {user.email}
    Desired Date:   {date}
    Desired timeTime:   {time}
    Location:   {location}
    Style:  {style}
    Do well to contact her as soon as possible!
    '''

    try:
        await send_email(background_tasks, subject, content)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")