# extensions.py
#
# WHY THIS FILE EXISTS:
# Both app.py and models/user.py need access to the same SQLAlchemy "db" object.
# If we created "db" directly inside app.py, models/user.py would have to import
# app.py to use it -- and app.py also needs to import models/user.py. That's a
# circular import, which crashes Python.
#
# The fix: put "db" in its own tiny standalone file that both app.py and
# models/user.py can import from safely.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
