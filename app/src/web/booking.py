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
        if not user:
            user = await user_controller.get_user_by_phone_number(phone_number)
    except Exception as e:
        user = None
    
    userMessage = None

    if not user:
        user = UserCreate(first_name=fullname.split()[0], last_name = " ".join(fullname.split()[1:]) if len(fullname.split()) > 1 else "", email=email, phone_number=phone_number, password="Pa$$word123")
        user = await user_controller.create_user(user)

        userMessage = f"""
        <html>
        <body>
            <div style="text-align:center; background-color:#ff0000; color:#ffffff; padding:20px;">
                <h1>4evabraids</h1>
            </div>
            <div style="padding:20px; font-family:Arial, sans-serif; font-size:14px;">
                <p>Hello <strong>{user.first_name}</strong>,</p>
                <p>You have successfully booked an appointment with the following details:</p>
                <ul>
                    <li><strong>Location:</strong> {location}</li>
                    <li><strong>Date:</strong> {date}</li>
                    <li><strong>Time:</strong> {time}</li>
                </ul>
                <p>We created an account for you to ease the booking process in the future. Here are your login details:</p>
                <ul>
                    <li><strong>Email:</strong> {email}</li>
                    <li><strong>Pa$$word123:</strong> password</li>
                </ul>
                <p>Thanks for choosing 4evabraids!</p>
            </div>
        </body>
        </html>
        """

        try:
            await send_email(background_tasks, "Account Created", userMessage, recipients=[email])
        except Exception as e:
            pass


    # Send booking details back to the user
    if not userMessage:
        userMessage = f"""
        <html>
        <body>
            <div style="text-align:center; background-color:#ff0000; color:#ffffff; padding:20px;">
                <h1>4evabraids</h1>
            </div>
            <div style="padding:20px; font-family:Arial, sans-serif; font-size:14px;">
                <p>Hello <strong>{user.first_name}</strong>,</p>
                <p>You have successfully booked an appointment with the following details:</p>
                <ul>
                    <li><strong>Location:</strong> {location}</li>
                    <li><strong>Date:</strong> {date}</li>
                    <li><strong>Time:</strong> {time}</li>
                </ul>
                <p>We will reach out to you shortly via calls or WhatsApp.</p>
                <p>Thanks for choosing 4evabraids!</p>
            </div>
        </body>
        </html>
        """

        try:
            await send_email(background_tasks, "Appointment Booked", userMessage, recipients=[email])
        except Exception as e:
            pass

    
    # Build up the message to be sent to braider
    subject = "You have a new appointment"
    content = f"""
    <html>
    <body>
        <div style="text-align:center; background-color:#ff0000; color:#ffffff; padding:20px;">
            <h1>4evabraids</h1>
        </div>
        <div style="padding:20px; font-family:Arial, sans-serif; font-size:14px;">
            <p><strong>Hello</strong>,</p>
            <p>You have a booking with the following details:</p>
            <ul>
                <li><strong>Name:</strong> {user.first_name} {user.last_name}</li>
                <li><strong>Phone:</strong> {user.phone_number}</li>
                <li><strong>Email:</strong> {user.email}</li>
                <li><strong>Desired Date:</strong> {date}</li>
                <li><strong>Desired Time:</strong> {time}</li>
                <li><strong>Location:</strong> {location}</li>
                <li><strong>Style:</strong> {style}</li>
            </ul>
            <p>Do well to contact her as soon as possible!</p>
        </div>
    </body>
    </html>
    """
    try:
        await send_email(background_tasks, subject, content)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: Could not send email. {str(e)}")