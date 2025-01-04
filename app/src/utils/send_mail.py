"""
This module povides a function to send mail to any email address using Fastapi
"""
from fastapi_mail import ConnectionConfig
from models.email import EmailemailSettings
from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema

emailSettings = EmailemailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME =emailSettings.MAIL_USERNAME,
    MAIL_PASSWORD =emailSettings.MAIL_PASSWORD,
    MAIL_FROM =emailSettings.MAIL_FROM,
    MAIL_FROM_NAME =emailSettings.MAIL_FROM_NAME,
    MAIL_PORT =emailSettings.MAIL_PORT,
    MAIL_SERVER =emailSettings.MAIL_SERVER,
    MAIL_STARTTLS = emailSettings.MAIL_STARTTLS,
    MAIL_SSL_TLS = emailSettings.MAIL_SSL_TLS,
    USE_CREDENTIALS = emailSettings.USE_CREDENTIALS,
    VALIDATE_CERTS = emailSettings.VALIDATE_CERTS,
)

async def send_email(background_tasks: BackgroundTasks, subject: str, content: str):
    message = MessageSchema(
        subject=subject,
        recipients=[*emailSettings.RECEIVERS_EMAIL],
        body=content,
        subtype="plain"
    )

    fm = FastMail(conf)
    try:
        background_tasks.add_task(fm.send_message, message)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))