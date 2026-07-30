# app.py
#
# DAY 6 UPDATE: Added signup/login/logout routes (prerequisite for booking),
# and the full appointment booking system (create, view, reschedule, cancel),
# all login-gated and ownership-checked per SCHEMA.md and API.md.

import os
from datetime import date, datetime
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user,
)
from dotenv import load_dotenv

from extensions import db
from models.user import User
from models.booking import Booking
from services.ai_service import analyze_symptoms
from data.doctor_repository import (
    filter_doctors,
    get_all_specialties,
    get_all_areas,
    get_doctor_by_id,
)

load_dotenv()

TIME_SLOTS = ["10:00 AM", "12:00 PM", "3:00 PM", "5:00 PM"]


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-fallback-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediguide.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # ----- Public Routes -----
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/symptom-checker", methods=["GET", "POST"])
    def symptom_checker():
        if request.method == "POST":
            symptoms = request.form.get("symptoms", "").strip()

            if len(symptoms) < 3:
                flash("Please describe your symptoms in a bit more detail.")
                return redirect(url_for("symptom_checker"))

            if len(symptoms) > 1000:
                flash("Please keep your description under 1000 characters.")
                return redirect(url_for("symptom_checker"))

            try:
                result = analyze_symptoms(symptoms)
            except Exception:
                flash("We couldn't analyze this right now. Please try again in a moment.")
                return redirect(url_for("symptom_checker"))

            return render_template("results.html", result=result)

        return render_template("symptom_checker.html")

    @app.route("/doctors")
    def doctors():
        selected_specialty = request.args.get("specialty", "").strip()
        selected_area = request.args.get("area", "").strip()

        matching_doctors = filter_doctors(
            specialty=selected_specialty or None,
            area=selected_area or None,
        )

        return render_template(
            "doctors.html",
            doctors=matching_doctors,
            specialties=get_all_specialties(),
            areas=get_all_areas(),
            selected_specialty=selected_specialty,
            selected_area=selected_area,
        )

    @app.route("/doctors/<doctor_id>")
    def doctor_detail(doctor_id):
        doctor = get_doctor_by_id(doctor_id)
        if doctor is None:
            return render_template("404.html"), 404
        return render_template("doctor_detail.html", doctor=doctor)

    # ----- Auth Routes -----
    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("home"))

        if request.method == "POST":
            phone_number = request.form.get("phone_number", "").strip()
            pin = request.form.get("pin", "").strip()
            confirm_pin = request.form.get("confirm_pin", "").strip()

            if not phone_number.isdigit() or len(phone_number) != 10:
                flash("Please enter a valid 10-digit phone number.")
                return redirect(url_for("signup"))

            if not pin.isdigit() or not (4 <= len(pin) <= 6):
                flash("PIN must be 4-6 digits.")
                return redirect(url_for("signup"))

            if pin != confirm_pin:
                flash("PINs do not match.")
                return redirect(url_for("signup"))

            existing = User.query.filter_by(phone_number=phone_number).first()
            if existing:
                flash("This phone number is already registered. Please log in instead.")
                return redirect(url_for("login"))

            new_user = User(phone_number=phone_number)
            new_user.set_pin(pin)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)
            flash("Account created successfully!")
            return redirect(url_for("home"))

        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("home"))

        if request.method == "POST":
            phone_number = request.form.get("phone_number", "").strip()
            pin = request.form.get("pin", "").strip()

            user = User.query.filter_by(phone_number=phone_number).first()

            if user is None or not user.check_pin(pin):
                flash("Invalid phone number or PIN.")
                return redirect(url_for("login"))

            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))

        return render_template("login.html")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("You've been logged out.")
        return redirect(url_for("home"))

    # ----- Booking Routes -----
    @app.route("/doctors/<doctor_id>/book", methods=["GET", "POST"])
    @login_required
    def book_appointment(doctor_id):
        doctor = get_doctor_by_id(doctor_id)
        if doctor is None:
            return render_template("404.html"), 404

        if request.method == "POST":
            date_str = request.form.get("appointment_date", "").strip()
            time_slot = request.form.get("time_slot", "").strip()

            try:
                appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Please choose a valid date.")
                return redirect(url_for("book_appointment", doctor_id=doctor_id))

            if appointment_date < date.today():
                flash("Please choose a future date.")
                return redirect(url_for("book_appointment", doctor_id=doctor_id))

            if time_slot not in TIME_SLOTS:
                flash("Please select a valid time slot.")
                return redirect(url_for("book_appointment", doctor_id=doctor_id))

            new_booking = Booking(
                user_id=current_user.id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                time_slot=time_slot,
                status="confirmed",
            )
            db.session.add(new_booking)
            db.session.commit()

            flash(f"Appointment booked with {doctor['name']} on {appointment_date.strftime('%d %b %Y')} at {time_slot}.")
            return redirect(url_for("my_appointments"))

        return render_template(
            "book_appointment.html",
            doctor=doctor,
            time_slots=TIME_SLOTS,
            min_date=date.today().isoformat(),
        )

    @app.route("/my-appointments")
    @login_required
    def my_appointments():
        user_bookings = (
            Booking.query.filter_by(user_id=current_user.id)
            .order_by(Booking.appointment_date.desc())
            .all()
        )

        # Attach doctor info (from JSON) to each booking for display
        bookings_with_doctors = []
        for booking in user_bookings:
            doctor = get_doctor_by_id(booking.doctor_id)
            bookings_with_doctors.append({"booking": booking, "doctor": doctor})

        return render_template("my_appointments.html", bookings=bookings_with_doctors)

    @app.route("/appointments/<int:booking_id>/reschedule", methods=["GET", "POST"])
    @login_required
    def reschedule_appointment(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            return render_template("404.html"), 404
        if booking.user_id != current_user.id:
            abort(403)

        doctor = get_doctor_by_id(booking.doctor_id)

        if request.method == "POST":
            date_str = request.form.get("appointment_date", "").strip()
            time_slot = request.form.get("time_slot", "").strip()

            try:
                appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                flash("Please choose a valid date.")
                return redirect(url_for("reschedule_appointment", booking_id=booking_id))

            if appointment_date < date.today():
                flash("Please choose a future date.")
                return redirect(url_for("reschedule_appointment", booking_id=booking_id))

            if time_slot not in TIME_SLOTS:
                flash("Please select a valid time slot.")
                return redirect(url_for("reschedule_appointment", booking_id=booking_id))

            booking.appointment_date = appointment_date
            booking.time_slot = time_slot
            db.session.commit()

            flash("Appointment rescheduled successfully.")
            return redirect(url_for("my_appointments"))

        return render_template(
            "reschedule.html",
            booking=booking,
            doctor=doctor,
            time_slots=TIME_SLOTS,
            min_date=date.today().isoformat(),
        )

    @app.route("/appointments/<int:booking_id>/cancel", methods=["POST"])
    @login_required
    def cancel_appointment(booking_id):
        booking = db.session.get(Booking, booking_id)
        if booking is None:
            return render_template("404.html"), 404
        if booking.user_id != current_user.id:
            abort(403)

        if booking.status == "cancelled":
            flash("This appointment is already cancelled.")
        else:
            booking.status = "cancelled"
            db.session.commit()
            flash("Appointment cancelled.")

        return redirect(url_for("my_appointments"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
