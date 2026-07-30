# MediGuide — Day 6 Summary

MVP Complete & Deployed | AB Talks 60-Day Claude Challenge Capstone

---

## ✅ What Was Completed Today

1. **Authentication pages built** (prerequisite gap closed from Day 3 scaffold)
   - `/signup` — phone number + PIN with confirm-PIN validation
   - `/login` — phone number + PIN authentication
   - `/logout` — session termination
   - Full validation: 10-digit phone check, 4-6 digit PIN check, duplicate
     phone detection, PIN mismatch detection

2. **Full appointment booking system (CRUD)**
   - `models/booking.py` — Booking table per SCHEMA.md
   - `/doctors/<id>/book` — create a booking (login-gated, future-date validated)
   - `/my-appointments` — list all of the logged-in user's bookings
   - `/appointments/<id>/reschedule` — update date/time (ownership-checked)
   - `/appointments/<id>/cancel` — cancel a booking (ownership-checked)
   - Cross-user protection verified: users cannot access or modify each
     other's bookings (403 Forbidden enforced)

3. **Required footer added**
   - "Built with Claude as part of the AB Talks 60-Day Claude AI Challenge."
   - Verified visible on every page, both locally and on the live deployed site

4. **Bug found and fixed: flash messages**
   - Signup/booking confirmation messages were being lost on redirect to
     pages without their own flash-rendering block
   - Fixed by centralizing flash message rendering in `base.html`, so every
     page shows confirmations consistently

5. **Deployed to Render (free tier)**
   - Live URL: **https://mediguide-ezpe.onrender.com**
   - Two deployment issues debugged and fixed:
     - `gunicorn "app:create_app()"` factory syntax wasn't recognized →
       switched to a dedicated `wsgi.py` entry point (`gunicorn wsgi:app`)
     - Database tables didn't exist on the fresh production server →
       added automatic `db.create_all()` inside `create_app()` so tables
       are created on every startup (safe, non-destructive)

6. **Full regression + live verification**
   - Complete signup → book → view → reschedule → cancel → logout flow
     tested and confirmed working on the LIVE deployed site, not just locally
   - All previously built features (symptom checker, doctor directory)
     re-verified working after today's changes

---

## 🚧 What Still Needs Polishing

- Review submission system not yet built (seeded reviews only) — originally
  scoped for Day 7
- No responsive/mobile polish pass yet — originally scoped for Day 8
- 404/error pages are functional but not yet visually polished
- Database on Render's free tier is not guaranteed persistent across
  redeploys (a known free-tier limitation) — acceptable for demo purposes,
  worth a note if continuing to build

---

## 🎯 What's Next

With the MVP now live and fully functional, remaining polish work
(reviews, responsive design, final UI pass) can proceed against a real,
working, deployed application rather than a local-only build — reducing
risk for the rest of the challenge.

---

## Files Changed/Added Today

| File | Status |
|---|---|
| `templates/signup.html` | New |
| `templates/login.html` | New |
| `models/booking.py` | New |
| `templates/book_appointment.html` | New |
| `templates/my_appointments.html` | New |
| `templates/reschedule.html` | New |
| `wsgi.py` | New (deployment fix) |
| `Procfile` | New (deployment config) |
| `app.py` | Modified — auth routes, booking CRUD, auto-db-init |
| `templates/base.html` | Modified — dynamic nav, centralized flash messages, required footer |
| `templates/doctor_detail.html` | Modified — real booking button |
| `static/css/style.css` | Modified — auth forms, appointments list, status badges |

---

## Live Demo

**https://mediguide-ezpe.onrender.com**

Note: the free-tier instance spins down after inactivity; the first
request after idle time may take 30-50 seconds to respond. This is
expected free-tier behavior, not an application bug.
