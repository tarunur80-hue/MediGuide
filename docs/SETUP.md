# MediGuide — Setup Guide

Version 1.0 | Day 3 Deliverable

This guide lets you (or anyone else) recreate the MediGuide development environment from scratch.

---

## Prerequisites

- **Python 3.9+** (confirmed working on 3.13.11)
- **Git** (for version control)
- A terminal (Git Bash on Windows, or Terminal on Mac/Linux)

---

## Step-by-Step Setup

### 1. Clone the repository
```bash
git clone https://github.com/tarunur80-hue/MediGuide.git
cd MediGuide
```

### 2. Create a virtual environment
A virtual environment keeps this project's Python packages isolated from your system Python and other projects.
```bash
python -m venv venv
```

### 3. Activate the virtual environment
**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```
**Mac/Linux:**
```bash
source venv/bin/activate
```
Your terminal prompt should now show `(venv)` at the start.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```
This installs Flask, Flask-SQLAlchemy, Flask-Login, python-dotenv, anthropic, and gunicorn — all pinned to tested versions.

### 5. Create your local environment file
```bash
cp .env.example .env
```
Then open `.env` in a text editor and fill in:
- `SECRET_KEY` — generate one with:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- `ANTHROPIC_API_KEY` — required starting Day 4 (can stay blank today)

### 6. Initialize the database
```bash
flask shell
```
Then inside the interactive shell:
```python
from extensions import db
db.create_all()
exit()
```
This creates `instance/mediguide.db` with the `users` table.

### 7. Run the application
```bash
flask run
```
Visit **http://127.0.0.1:5000** in your browser. You should see the MediGuide homepage.

---

## Verifying Everything Works

| Check | How to Verify |
|---|---|
| App runs without errors | `flask run` shows "Running on http://127.0.0.1:5000" with no tracebacks |
| Homepage loads | Visiting the URL shows navbar, hero text, and footer |
| Static files load | Page is styled (navy/teal colors, proper fonts) — not plain unstyled HTML |
| Database exists | `find . -name "*.db"` shows `instance/mediguide.db` |
| Users table exists | Querying `sqlite_master` shows a `users` table |

---

## Common Setup Issues

| Problem | Fix |
|---|---|
| `flask: command not found` | Virtual environment isn't activated — re-run the activate command |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed, or wrong environment active — check `which python` points inside `venv` |
| Port 5000 already in use | Run `flask run -p 5001` instead |
| Templates not rendering / TemplateNotFound | Confirm you're running `flask run` from the project root, and the folder is named exactly `templates` |
| `.env` values not loading | Confirm `.env` (not `.env.example`) exists in the project root and `load_dotenv()` is called before reading any variable |
