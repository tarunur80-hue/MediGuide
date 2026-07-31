# models/review.py
#
# WHAT THIS FILE DOES:
# Defines the "Review" table -- one row per review a logged-in user submits
# for a doctor. Matches SCHEMA.md: id, user_id (FK), doctor_id, rating,
# text, created_at.

from datetime import datetime, timezone
from extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doctor_id = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Review id={self.id} doctor_id={self.doctor_id} rating={self.rating}>"
