# MediGuide — Project Structure (Updated Day 3)

Version 1.1 | Originally created Day 2, updated Day 3 with implementation details

---

## 1. Actual Folder Structure (as of Day 3)

```
MediGuide/
│
├── app.py                     # Flask app factory: config, db init, login manager, routes
├── extensions.py               # Shared SQLAlchemy `db` instance (avoids circular imports)
├── requirements.txt            # Pinned dependency list (pip freeze output)
├── .env                        # Local secrets: SECRET_KEY, ANTHROPIC_API_KEY (gitignored)
├── .env.example                # Template for .env, safe to commit
├── .gitignore                  # Excludes venv, __pycache__, .env, instance/, mediguide.db
├── README.md                   # Project overview (finalized Day 10)
│
├── /venv                      # Python virtual environment (gitignored, not committed)
├── /instance                  # Auto-created by Flask; holds mediguide.db (gitignored)
│   └── mediguide.db
│
├── /models
│   ├── __init__.py             # Makes "models" a Python package
│   └── user.py                 # User model: id, phone_number, pin_hash, created_at
│
├── /services                  # (Empty today — populated Day 4 with ai_service.py)
│
├── /data                      # (Empty today — populated Day 5 with doctors.json + repository)
│
├── /templates
│   ├── base.html                # Shared layout: navbar, footer, block structure
│   └── index.html               # Homepage content (extends base.html)
│
├── /static
│   ├── /css
│   │   └── style.css             # Full design system: colors, navbar, hero, footer, responsive rules
│   └── /js
│       └── main.js               # Placeholder for future interactions (Day 4+)
│
└── /docs                      # Planning & design documentation
    ├── ARCHITECTURE.md
    ├── SCHEMA.md
    ├── API.md
    ├── UI-WIREFRAMES.md
    ├── PROJECT-STRUCTURE.md      (this file)
    ├── SETUP.md                   (Day 3)
    ├── ENVIRONMENT.md             (Day 3)
    └── DAY3-SUMMARY.md            (Day 3)
```

---

## 2. What Changed Since Day 2's Version

| Item | Day 2 Plan | Day 3 Reality | Why |
|---|---|---|---|
| Database file location | Assumed project root | Actually lives in `/instance` | This is Flask's default convention when using a relative SQLite URI — not a deviation, just how Flask behaves. No action needed; already gitignored. |
| `extensions.py` | Not explicitly planned | Added | Needed to avoid a circular import between `app.py` and `models/user.py`. Both need the same `db` object, so it lives in its own small file. Purely an implementation detail — no scope change. |
| `.env.example` | Not explicitly planned | Added | Best practice so the real `.env` structure is documented and shareable without exposing real secrets. |

No other deviations. `/services` and `/data` remain empty today exactly as scheduled — they're built Day 4 and Day 5 respectively.

---

## 3. Why `extensions.py` Exists (Explained Simply)

Both `app.py` and `models/user.py` need to use the same database connection object (`db`). If `db` were created directly inside `app.py`, then `models/user.py` would need to import `app.py` to use it — but `app.py` also needs to import `models/user.py` to register the User model. Python can't resolve two files that need each other at the same time (a "circular import"), so `db` lives in its own neutral file that both can import from safely.

---

## 4. Confirmed Working (Day 3)

- ✅ Folder structure matches this document exactly
- ✅ `flask run` starts with no errors
- ✅ Homepage renders with correct styling
- ✅ Database creates successfully with the `users` table
- ✅ No unused or orphaned files
