# MediGuide — Project Structure

Version 1.0 | Day 2 Deliverable

---

## 1. Folder Structure

```
MediGuide/
│
├── app.py                     # Flask app factory, route registrations, config
├── requirements.txt           # Python dependencies (generated via pip freeze)
├── .env                       # ANTHROPIC_API_KEY, SECRET_KEY (gitignored, never committed)
├── .gitignore                 # Excludes venv, __pycache__, .env, mediguide.db
├── Procfile                   # Deployment start command (added Day 9)
├── README.md                  # Project overview, setup steps, live link (finalized Day 10)
│
├── /models                    # SQLAlchemy models — one file per entity
│   ├── user.py                 # User model (Day 3)
│   ├── booking.py               # Booking model (Day 6)
│   └── review.py                # Review model (Day 7)
│
├── /services                  # Business logic isolated from routes
│   └── ai_service.py            # Claude API integration (Day 4)
│
├── /data                      # Static/mock reference data + access helpers
│   ├── doctors.json             # Mock doctor/hospital dataset (Day 5)
│   └── doctor_repository.py     # Query/filter helpers for doctors.json (Day 5)
│
├── /templates                 # Jinja2 HTML templates
│   ├── base.html                 # Shared layout: navbar, footer (Day 2)
│   ├── index.html                # Homepage (Day 2)
│   ├── signup.html               # Signup form (Day 3)
│   ├── login.html                # Login form (Day 3)
│   ├── symptom_checker.html      # Symptom input form (Day 4)
│   ├── results.html              # AI results display (Day 4)
│   ├── doctors.html              # Directory grid + filters (Day 5)
│   ├── doctor_detail.html        # Doctor profile + reviews + booking entry (Day 5, updated Day 7)
│   ├── book_appointment.html     # Booking form (Day 6)
│   ├── my_appointments.html      # User's bookings list (Day 6)
│   ├── reschedule.html           # Reschedule form (Day 6)
│   ├── 404.html                  # Not-found error page (Day 8)
│   └── error.html                # Generic server error page (Day 8)
│
├── /static
│   ├── /css
│   │   └── style.css             # Shared design system: colors, spacing, components
│   └── /js
│       └── main.js               # Star ratings, loading states, small interactions
│
└── /docs                       # Project documentation (this Day 2 deliverable set)
    ├── ARCHITECTURE.md
    ├── SCHEMA.md
    ├── API.md
    ├── UI-WIREFRAMES.md
    └── PROJECT-STRUCTURE.md
```

---

## 2. Rationale for Each Major Folder

- **`/models`** — Keeps database structure isolated from route logic. Each entity (User, Booking, Review) gets its own file so the schema stays easy to navigate as it grows across Days 3, 6, and 7.
- **`/services`** — Isolates external API logic (Claude) from Flask routes. This means `ai_service.py` can be tested or modified independently without touching route handlers — a clean separation of concerns.
- **`/data`** — Groups all mock/reference data together with its access logic. Since doctors.json is not a database table, keeping its repository helper alongside it makes the "who reads this file" relationship obvious.
- **`/templates`** — Standard Flask convention (Flask looks for this exact folder name). All pages extend `base.html` so navbar/footer changes only need to happen in one place.
- **`/static`** — Standard Flask convention for CSS/JS/images. Keeping `css` and `js` as subfolders (rather than flat files) keeps this scalable if more assets are added later.
- **`/docs`** — Keeps all planning/design documentation in the repo itself (versioned alongside code), so future days — and anyone reviewing the project — can see the full design reasoning without hunting through chat history.

---

## 3. Where Future Code Will Live (Day-by-Day Mapping)

| Day | New Files/Folders |
|---|---|
| Day 2 (today) | app.py, base.html, index.html, style.css, main.js, /docs/*.md |
| Day 3 | models/user.py, templates/signup.html, templates/login.html |
| Day 4 | services/ai_service.py, templates/symptom_checker.html, templates/results.html |
| Day 5 | data/doctors.json, data/doctor_repository.py, templates/doctors.html, templates/doctor_detail.html |
| Day 6 | models/booking.py, templates/book_appointment.html, templates/my_appointments.html, templates/reschedule.html |
| Day 7 | models/review.py (review section added to doctor_detail.html) |
| Day 8 | templates/404.html, templates/error.html (polish pass across all templates + style.css) |
| Day 9 | Procfile (deployment config) |
| Day 10 | README.md finalized (no new app code) |

---

## 4. Why This Structure Was Chosen

- **Matches Flask conventions** (`templates/`, `static/`) so no custom configuration is needed — reduces setup friction and debugging risk.
- **Separates concerns cleanly**: models (data), services (external logic), data (mock reference), templates/static (presentation). This means each day's work touches a predictable, isolated part of the codebase.
- **Scales without restructuring**: every day from Day 3–9 only adds new files into existing folders — no folder reorganization needed mid-build, which protects against wasted time.
- **Fresh-conversation friendly**: because the structure is explicit and documented in `/docs`, a new AI conversation on any future day can understand the whole project layout immediately without needing to explore the codebase from scratch.
