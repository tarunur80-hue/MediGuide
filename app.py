# app.py
#
# WHAT THIS FILE DOES (in plain English):
# This is the entry point of our entire application. When you run "flask run",
# Python starts here. This file:
#   1. Creates the Flask app itself
#   2. Loads secret configuration (API keys, secret key) from the .env file
#   3. Connects our SQLite database
#   4. Sets up Flask-Login (so we can log users in/out later)
#   5. Defines our first route: the homepage ("/")
#
# Today (Day 3), the homepage just proves everything is wired together
# correctly -- this is our "Hello World." Authentication routes (signup/login)
# are scaffolded today too, but the actual signup/login PAGES come in Day 3's
# second half / early Day 4 depending on how far we get.

import os
from flask import Flask, render_template
from flask_login import LoginManager
from dotenv import load_dotenv

from extensions import db
from models.user import User

# Load variables from the .env file (like ANTHROPIC_API_KEY, SECRET_KEY)
# into the environment, so os.environ.get(...) can find them.
load_dotenv()


def create_app():
    """
    This is called an "app factory" pattern. Instead of creating the Flask
    app directly at the top of the file, we wrap it in a function. This is
    a Flask best practice -- it makes testing and configuration easier later,
    without changing how we run the app today.
    """
    app = Flask(__name__)

    # SECRET_KEY is used by Flask to securely sign session cookies (so users
    # stay logged in). It must be a random, secret string -- never hardcoded
    # in real code, which is why we load it from .env.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-fallback-key")

    # This tells SQLAlchemy where our database file lives. "sqlite:///" means
    # a local file-based database named mediguide.db in our project folder.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mediguide.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # turns off an unneeded feature that just uses extra memory

    # Connect our shared "db" object (from extensions.py) to this specific app.
    db.init_app(app)

    # ----- Flask-Login setup -----
    login_manager = LoginManager()
    login_manager.login_view = "login"  # if someone tries to access a protected page, send them here (built Day 3/4)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """
        Flask-Login calls this automatically on every request to figure out
        WHO the currently logged-in user is, based on their session cookie.
        We just look them up in the database by id.
        """
        return db.session.get(User, int(user_id))

    # ----- Routes -----
    @app.route("/")
    def home():
        return render_template("index.html")

    return app


# This block only runs when you type "python app.py" directly.
# When using "flask run" instead, Flask finds create_app() automatically,
# and this block is skipped -- which is exactly what we want for local dev.
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
