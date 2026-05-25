import logging
import smtplib
from email.mime.text import MIMEText
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..config.database import get_db
from ..config.settings import settings
from ..models.contact import ContactRequest, ContactMessageInDB

from fastapi.concurrency import run_in_threadpool

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contact", tags=["Contact"])

def send_contact_email(name: str, email: str, phone: Optional[str], message: str):
    """Send a plain text email to the maintainer using SMTP."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP credentials not set. Email not sent.")
        raise Exception("SMTP credentials are not configured on the server.")

    subject = f"New Career Help Inquiry from {name}"
    body = f"""
New contact form submission from CareerForge AI:

Name: {name}
Email: {email}
Phone: {phone if phone else 'Not provided'}

Message:
{message}

---
This email was sent automatically from CareerForge AI.
    """
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.SMTP_USER
    msg['To'] = settings.CONTACT_EMAIL
    msg.add_header('Reply-To', email)

    # Do not catch exceptions here so the caller knows if it failed
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        logger.info(f"Contact email sent to {settings.CONTACT_EMAIL}")

@router.post("")
async def submit_contact_form(request: ContactRequest):
    """
    Handle contact form submission:
    1. Save to MongoDB (always)
    2. Send Email synchronously to ensure delivery before responding
    """
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        # 1. Save to DB
        message_doc = ContactMessageInDB(**request.model_dump()).model_dump()
        await db.contact_messages.insert_one(message_doc)
        
        # 2. Trigger email (awaited so we know if it succeeded)
        await run_in_threadpool(send_contact_email, request.name, request.email, request.phone, request.message)
        
        return {"status": "success", "message": "Your inquiry has been sent successfully!"}
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email. Please check server configuration.")
