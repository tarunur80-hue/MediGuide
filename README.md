# MediGuide

**Know what's wrong. Know what to do next.**

MediGuide is an AI-guided health companion that helps people understand their symptoms, find the right doctor nearby, and book appointments — all in one place. Built as the capstone project for the [AB Talks 60-Day Claude AI Challenge](https://www.linkedin.com/in/anilbajpai/), mentored by Anil Bajpai.

🔗 **Live app:** [mediguide-ezpe.onrender.com](https://mediguide-ezpe.onrender.com)

---

## Features

- 🩺 **Symptom Checker** — describe symptoms in plain language and get a structured, explained assessment (condition, reasoning, severity, and next steps) with a safety-first disclaimer on every response
- 🏥 **Doctor & Hospital Directory** — browse and filter 24 doctors across 9 specialties and 3 areas, no account required
- 📅 **Appointment Booking** — full booking lifecycle: book, view, reschedule, and cancel appointments
- ⭐ **Reviews & Ratings** — read existing reviews or submit your own; ratings recalculate live
- 🔐 **Simple Authentication** — phone number + PIN signup/login, no complex passwords required

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Authentication | Flask-Login, Werkzeug password hashing |
| Security | Flask-WTF (CSRF), Flask-Limiter (rate limiting) |
| Frontend | HTML, CSS, vanilla JavaScript, Jinja2 templates |
| Hosting | Render (free tier) |

## Screenshots

See the app live at [mediguide-ezpe.onrender.com](https://mediguide-ezpe.onrender.com) — browse the symptom checker, doctor directory, and booking flow directly.

---

## Running Locally

### Prerequisites
- Python 3.9+
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/tarunur80-hue/MediGuide.git
cd MediGuide

# Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate      # Windows (Git Bash)
# source venv/bin/activate        # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Generate a SECRET_KEY:
python -c "import secrets; print(secrets.token_hex(32))"
# Paste the output into .env as SECRET_KEY=...

# Run the app
flask run
```

Visit `http://127.0.0.1:5000` in your browser. The database and all tables are created automatically on first run — no manual setup required.

### Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `SECRET_KEY` | Yes | Signs session cookies |
| `ANTHROPIC_API_KEY` | No (optional) | Only needed if swapping in the real Claude API symptom checker (see `services/ai_service.py`) |
| `FLASK_ENV` | No | Set to `production` in production hosting to enable secure cookies |

See `docs/ENVIRONMENT.md` for full details.

---

## Project Structure

```
MediGuide/
├── app.py                 # Flask app factory, routes, security config
├── wsgi.py                 # Production entry point (gunicorn)
├── extensions.py            # Shared SQLAlchemy instance
├── requirements.txt
├── models/                 # Database models (User, Booking, Review)
├── services/                # AI symptom-checking logic
├── data/                    # Mock doctor/hospital dataset + query helpers
├── templates/                # Jinja2 HTML templates
├── static/                   # CSS, JS, images/favicon
└── docs/                      # Full project documentation (PRD, architecture, etc.)
```

Full architectural details, database schema, and API documentation live in [`/docs`](./docs).

---

## Security

- CSRF protection on every form
- Rate limiting on login, signup, and review submission
- Hardened session cookies (HttpOnly, SameSite, Secure-in-production)
- Passwords (PINs) are hashed, never stored in plain text
- Open-redirect protection on login redirects

## Known Limitations

- The AI symptom checker currently runs on rule-based placeholder logic rather than a live Claude API call (see `docs/DAY4-SUMMARY.md` for the reasoning — the real Claude API integration is fully written and ready to activate, just gated behind adding API credits)
- Render's free tier does not guarantee persistent database storage across redeploys
- Doctor and hospital data is illustrative/mock data, not real medical providers

## License

This project is licensed under the MIT License — see [LICENSE](./LICENSE) for details.

## Acknowledgments

Built with [Claude](https://claude.com) as part of the AB Talks 60-Day Claude AI Challenge.
