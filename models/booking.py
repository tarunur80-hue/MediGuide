# models/booking.py
#
# WHAT THIS FILE DOES:
# Defines the "Booking" table -- one row per appointment a user creates.
# Matches SCHEMA.md: id, user_id (FK), doctor_id, appointment_date,
# time_slot, status, created_at.

from datetime import datetime, timezone
from extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doctor_id = db.Column(db.String(20), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="confirmed")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Booking id={self.id} doctor_id={self.doctor_id} status={self.status}>"
