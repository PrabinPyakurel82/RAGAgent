from fastapi import APIRouter,Depends,Form
from sqlalchemy.orm import Session
import smtplib
from email.mime.text import MIMEText

from app.core.schemas import BookingCreate
from app.core.models import Booking
from app.core.database import get_db
from app.core.config import settings


router = APIRouter()


@router.post("/booking/")
def book_interview(booking:BookingCreate=Form(...),db:Session=Depends(get_db)):

    new_booking = Booking(
        full_name = booking.full_name,
        email = booking.email,
        timestamp = booking.timestamp
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    msg = MIMEText(f"New interview booking:\n\nName: {booking.full_name}\nEmail: {booking.email}\nDate: {booking.timestamp}\n")
    msg["Subject"] = "New Interview Booking"
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = settings.EMAIL_ADDRESS


    try:
       with smtplib.SMTP("smtp.gmail.com",587) as server:
           server.starttls()
           server.login(settings.EMAIL_ADDRESS,settings.EMAIL_APP_PASSWORD)
           server.send_message(msg)
    except Exception as e:
        return {"status": "failed", "reason": str(e)}
    
    return {"status": "success", "message": "Booking confirmed and email sent."}
