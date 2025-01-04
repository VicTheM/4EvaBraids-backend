from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr
from utils.send_mail import send_email

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/")
async def create_appointment(background_tasks: BackgroundTasks, email: EmailStr):
    name = "John Doe"
    phone = "08012345678"
    date = "2021-12-01"
    time = "10:00 AM"
    location = "Lekki Phase 1"
    style = "Braids"

    subject = "You have a new appointment"
    content = f'''
    Hello, you have a booking with the following details:
    
    Name:   {name}
    Phone:  {phone}
    Email:  {email}
    Date:   {date}
    Time:   {time}
    Location:   {location}
    Style:  {style}

    Do well to contact her as soon as possible!
    '''

    try:
        await send_email(background_tasks, subject, content)
        # Save order to database in the future
        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"message": "An error occurred while sending the email."}