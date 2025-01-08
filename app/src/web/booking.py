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
from models.user import UserCreate

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/")
async def create_appointment(background_tasks: BackgroundTasks, location: str = "unknown",
                             style: str = "Unknown", date: str = "01-01-2025", time: str = "00.00am",
                             fullname: str = "Unknown", email: str = "fake@gmail.com", phone_number: str = "Unknown"):
    """
    Create an appointment. Automatically create account if not logged in
    """
    
    try:
        user = await user_controller.get_user_by_email(email)
    except Exception as e:
        user = await user_controller.get_user_by_phone_number(phone_number)
    
    userMessage = None

    if not user:
        user = UserCreate(first_name=fullname.split()[0], last_name=" ".join(fullname.split()[1:]),
                             email=email, phone_number=phone_number, password="password")
        user = await user_controller.create_user(user)

        userMessage = f'''
        Hello {user.first_name}, you have been successfully booked an appiontment with the following details:
        Location: {location}
        Time: {time}

        We created an account for you to ease booking process in the future, here is your login details:
        Email: {email}
        Password: password
        '''

        try:
            await send_email(background_tasks, "Account Created", userMessage, recipients=[email])
        except Exception as e:
            pass


    # Send booking details back to the user
    if not userMessage:
        userMessage = f'''
        Hello {user.first_name}, you have been successfully booked an appiontment with the following details:
        Location: {location}
        Time: {time}

        We will reach out to you shortly via calls or Whatsapp
        '''

        try:
            await send_email(background_tasks, "Appointment Booked", userMessage, recipients=[email])
        except Exception as e:
            pass

    
    # Build up the message to be sent to braider
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