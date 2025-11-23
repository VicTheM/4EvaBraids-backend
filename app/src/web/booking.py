"""
This file defines the route used to book an appointment
"""
from fastapi import APIRouter
from fastapi import BackgroundTasks
from utils.send_mail import send_email
from fastapi import HTTPException
from controllers import user as user_controller
from models.user import UserCreate
from service.booking import build_account_created_email, build_booking_email, build_braider_email
from config import settings

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
        if not user:
            user = await user_controller.get_user_by_phone_number(phone_number)
    except Exception as e:
        user = None
    
    userMessage = None
    if not user:
        user = UserCreate(first_name=fullname.split()[0], last_name = " ".join(fullname.split()[1:]) if len(fullname.split()) > 1 else "", email=email, phone_number=phone_number, password=settings.USERPASSWORD)
        user = await user_controller.create_user(user)

        userMessage = build_account_created_email(user, location, date, time, email)
        try:
            await send_email(background_tasks, "Account Created", userMessage, recipients=[email])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: Could not send email. {str(e)}")
    else:
        userMessage = build_booking_email(user, location, date, time)
        try:
            await send_email(background_tasks, "Appointment Booked", userMessage, recipients=[email])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: Could not send email. {str(e)}")

    # Notify braider
    braiderMessage = build_braider_email(user, location, style, date, time)
    try:
        await send_email(background_tasks, "You have a new appointment", braiderMessage)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: Could not send email. {str(e)}")