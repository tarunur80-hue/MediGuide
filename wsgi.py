# wsgi.py
#
# WHAT THIS FILE DOES:
# Production servers like gunicorn expect a simple, ready-made app object
# to import (not a function to call). This file creates that object once
# by calling our app factory, so gunicorn can just do: gunicorn wsgi:app

from app import create_app

app = create_app()
