# MediGuide — Environment Configuration

Version 1.0 | Day 3 Deliverable

---

## Environment Variables

These live in a local `.env` file (never committed to Git — see `.env.example` for the template).

| Variable | Purpose | Required By | Example Value |
|---|---|---|---|
| `SECRET_KEY` | Signs Flask session cookies so login sessions can't be tampered with | Day 3 (Flask-Login setup) | Random 64-char hex string |
| `ANTHROPIC_API_KEY` | Authenticates calls to the Claude API for the AI symptom checker | Day 4 (AI Symptom Checker) | `sk-ant-...` (from console.anthropic.com) |

**How they're loaded:** `app.py` calls `load_dotenv()` at the top of the file, which reads `.env` and makes these values available via `os.environ.get(...)`.

---

## Development Tools & Versions

| Tool | Version Confirmed Working | Purpose |
|---|---|---|
| Python | 3.13.11 | Runtime for the entire backend |
| pip | 26.1.2 | Installs Python packages |
| Flask | 3.1.3 | Web framework — routing, templating, request handling |
| Flask-SQLAlchemy | 3.1.1 | ORM — defines database tables as Python classes |
| Flask-Login | 0.6.3 | Session/login management |
| python-dotenv | 1.2.2 | Loads `.env` variables into the app |
| anthropic | 0.119.0 | Official Claude API SDK (used from Day 4) |
| gunicorn | 26.0.0 | Production WSGI server (used from Day 9 deployment) |
| Werkzeug | 3.1.8 | Underlying WSGI toolkit Flask is built on (installed automatically with Flask); also provides password hashing |
| SQLAlchemy | 2.0.51 | Underlying ORM engine that Flask-SQLAlchemy wraps |

Full pinned list lives in `requirements.txt` (generated via `pip freeze`).

---

## Local Configuration Summary

| Setting | Value | Where It's Set |
|---|---|---|
| Database engine | SQLite | `app.config["SQLALCHEMY_DATABASE_URI"]` in `app.py` |
| Database file location | `instance/mediguide.db` | Auto-created by Flask's default instance folder convention |
| Debug mode | Off by default (`app.run(debug=True)` only when running `python app.py` directly; `flask run` uses Flask CLI defaults) | `app.py` |
| Session security | Cookie signed using `SECRET_KEY` | `app.config["SECRET_KEY"]` in `app.py` |

---

## What's NOT Configured Yet (By Design)

These are intentionally deferred to later days per the Implementation Blueprint:

| Item | Deferred To | Why |
|---|---|---|
| Real `ANTHROPIC_API_KEY` value | Day 4 | AI symptom checker isn't built until Day 4 |
| Production `SECRET_KEY` (separate from local dev key) | Day 9 | Set directly in the hosting platform's environment variables at deploy time |
| `FLASK_ENV` / production config toggles | Day 9 | Not needed until deployment |
| Gunicorn `Procfile` | Day 9 | Only needed for deployment, not local development |
