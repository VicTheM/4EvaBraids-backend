"""Helper functions to build email bodies for different scenarios"""
from typing import List

def build_email_body(title: str, body: str) -> str:
    """Generic HTML wrapper for emails"""
    return f"""
    <html>
    <body>
        <div style="text-align:center; background-color:#C5A02E; color:#ffffff; padding:20px;">
            <h1>{title}</h1>
        </div>
        <div style="padding:20px; font-family:Arial, sans-serif; font-size:14px;">
            {body}
        </div>
    </body>
    </html>
    """

def build_account_created_email(user, location, date, time, email) -> str:
    body = f"""
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
            <li><strong>Password:</strong> Pa$$word123</li>
        </ul>
        <p>Thanks for choosing 4evabraids!</p>
    """
    return build_email_body("4evabraids", body)

def build_booking_email(user, location, date, time) -> str:
    body = f"""
        <p>Hello <strong>{user.first_name}</strong>,</p>
        <p>You have successfully booked an appointment with the following details:</p>
        <ul>
            <li><strong>Location:</strong> {location}</li>
            <li><strong>Date:</strong> {date}</li>
            <li><strong>Time:</strong> {time}</li>
        </ul>
        <p>We will reach out to you shortly via calls or WhatsApp.</p>
        <p>Thanks for choosing 4evabraids!</p>
    """
    return build_email_body("4evabraids", body)

def build_braider_email(user, location, style, date, time) -> str:
    body = f"""
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
    """
    return build_email_body("4evabraids", body)
