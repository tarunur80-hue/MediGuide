# models/user.py
#
# WHAT THIS FILE DOES:
# Defines the "User" table in our database using SQLAlchemy. Instead of writing
# raw SQL like "CREATE TABLE users (...)", we write a Python class, and
# SQLAlchemy translates it into the actual database table for us.
#
# This matches the schema locked in SCHEMA.md on Day 2:
#   id | phone_number (unique) | pin_hash | created_at
#
# It also implements Flask-Login's required interface (via UserMixin) so
# Flask-Login knows how to check if a user "is_authenticated", get their
# "id", etc. -- without us having to write that logic ourselves.

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    pin_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_pin(self, raw_pin):
        """Hashes the PIN before storing it. We NEVER store the raw PIN."""
        self.pin_hash = generate_password_hash(raw_pin)

    def check_pin(self, raw_pin):
        """Compares a login attempt's PIN against the stored hash."""
        return check_password_hash(self.pin_hash, raw_pin)

    def __repr__(self):
        return f"<User id={self.id} phone_number={self.phone_number}>"
