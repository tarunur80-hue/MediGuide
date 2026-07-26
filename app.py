# app.py
#
# WHAT THIS FILE DOES (in plain English):
# This is the entry point of our entire application. When you run "flask run",
# Python starts here. This file:
#   1. Creates the Flask app itself
#   2. Loads secret configuration (API keys, secret key) from the .env file
#   3. Connects our SQLite database
#   4. Sets up Flask-Login (so we can log users in/out later)
#   5. Defines our routes: homepage, symptom checker, and (NEW today)
#      the doctor directory and doctor detail pages
#
# DAY 5 UPDATE: Added the Doctor & Hospital Directory (hero feature) --
# public browsing with specialty/area filters, plus a detail page showing
# bio, reviews, and placeholders for booking (Day 6) and review submission
# (Day 7).

import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager
from dotenv import load_dotenv

from extensions import db
from models.user import User
from services.ai_service import analyze_symptoms
from data.doctor_repository import (
    filter_doctors,
    get_all_specialties,
    get_all_areas,
    get_doctor_by_id,
)

load_dotenv()


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

    # ----- Routes -----
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/symptom-checker", methods=["GET", "POST"])
    def symptom_checker():
        """
        GET: show the empty symptom input form.
        POST: validate the submitted symptoms, run analyze_symptoms(), and
              render the results page with the structured AI response.
        """
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
        """
        Public doctor/hospital directory. Supports optional ?specialty= and
        ?area= query params for filtering. No login required.
        """
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
        """
        Full profile page for a single doctor: bio, rating, fee, and reviews.
        Returns a 404 page if the doctor_id doesn't exist in doctors.json.
        """
        doctor = get_doctor_by_id(doctor_id)
        if doctor is None:
            return render_template("404.html"), 404

        return render_template("doctor_detail.html", doctor=doctor)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
