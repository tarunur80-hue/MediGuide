# MediGuide — Day 8 Summary

Testing, Debugging & Production Optimization | AB Talks 60-Day Claude Challenge Capstone

---

## ✅ What Was Completed Today

A full senior-level review (QA Engineer, Security Reviewer, Performance
Engineer, Software Engineer) was conducted across the entire application,
followed by fixes for every issue found — each one verified with real
automated tests, not just code inspection.

### 🔴 Security Hardening
1. **CSRF protection** added to every POST form (signup, login, logout,
   booking, reschedule, cancel, review submission) via Flask-WTF.
   Verified: a POST request without a valid CSRF token is now correctly
   rejected (400 Bad Request); a POST with a valid token succeeds normally.
2. **Rate limiting** added to login (15/hour), signup (10/hour), and review
   submission (20/hour) via Flask-Limiter — directly mitigates PIN
   brute-forcing given the small 4-6 digit PIN space. Verified: repeated
   wrong-PIN login attempts are blocked at the 16th try.
3. **Session cookie hardening**: `HttpOnly` (blocks JS access to the
   session cookie), `SameSite=Lax` (blocks cross-site cookie sending),
   `Secure` in production (HTTPS-only).
4. **Open-redirect protection** on the login `?next=` parameter — an
   attacker-supplied external URL is now ignored and the user is safely
   redirected to the homepage instead. Verified with a real test.
5. **User enumeration prevention** confirmed already correct: login shows
   the same generic error for "wrong phone" and "wrong PIN."

### 🟠 Bug Fixes
6. Fixed a crash risk in the doctor avatar initial logic for any doctor
   with a single-word (no-space) name — replaced with a safe helper
   function, verified with a test doctor entry.
7. **Caught and fixed a bug introduced by today's own CSRF rollout**: the
   symptom checker form was initially missed when adding CSRF tokens,
   which would have broken that entire feature in production. Found
   during my own end-to-end test pass and fixed before it ever reached you.
8. Fixed cross-user booking access — verified both reschedule and cancel
   correctly return 403 Forbidden when a different logged-in user tries
   to access someone else's appointment.
9. Added defensive handling for a booking/review referencing a doctor_id
   that no longer exists in doctors.json.

### 🟠 Performance
10. **Fixed an N+1 database query problem** on the doctor directory page:
    previously ran one review-count query per doctor card (24 queries for
    24 doctors on an unfiltered page load). Now runs a single query and
    groups results in Python. Verified: query count dropped from 24 to 1.

### 🟢 Reliability
11. Added proper **403, 500, and 429 error pages** (previously only 404
    existed) with consistent styling matching the rest of the app.
12. Added `db.session.rollback()` in the 500 handler so a failed database
    transaction can't leave the app in a broken state for subsequent requests.

### 🟢 Accessibility
13. Star rating widget is now fully keyboard-navigable (Tab + Enter/Space)
    with proper ARIA roles for screen reader users.
14. Added `autocomplete` attributes to phone/PIN fields.

### Code Quality
15. Extracted duplicate date/time validation logic into a single shared
    `validate_booking_datetime()` helper.

---

## Full End-to-End Verification (Live Production Site)

Every core user journey was tested and confirmed working on
**https://mediguide-ezpe.onrender.com** after deployment:

- ✅ Symptom checker (mild and serious cases)
- ✅ Doctor directory browsing and filtering
- ✅ Signup with success confirmation
- ✅ Appointment booking with confirmation
- ✅ Reschedule with confirmation
- ✅ Cancel with status update
- ✅ Review submission with live rating recalculation
- ✅ Logout with confirmation

No regressions.

---

## Known Limitation (Documented, Not a Bug)

Render's free tier does not guarantee persistent disk storage across
redeploys — the SQLite database may reset when the service redeploys or
restarts after extended inactivity. This is an accepted limitation for a
free-tier capstone demo.

---

## 🎯 What Remains Before Final Launch

- Final documentation pass (README, PRD alignment check)
- Demo script rehearsal
- Optional: broader manual testing on real mobile devices

---

## Files Changed Today

| File | Status |
|---|---|
| `app.py` | Modified — CSRF, rate limiting, session hardening, N+1 fix, error handlers, shared validation helper |
| `requirements.txt` | Modified — added Flask-WTF, Flask-Limiter |
| `templates/base.html` | Modified — CSRF token on logout form |
| `templates/signup.html` | Modified — CSRF token, autocomplete attributes |
| `templates/login.html` | Modified — CSRF token, autocomplete attributes |
| `templates/book_appointment.html` | Modified — CSRF token |
| `templates/reschedule.html` | Modified — CSRF token |
| `templates/my_appointments.html` | Modified — CSRF token on cancel form |
| `templates/symptom_checker.html` | Modified — CSRF token (bug fix) |
| `templates/doctor_detail.html` | Modified — CSRF token, ARIA roles, safe avatar helper |
| `templates/doctors.html` | Modified — safe avatar helper |
| `templates/403.html` | New |
| `templates/500.html` | New |
| `templates/429.html` | New |
| `static/js/main.js` | Modified — keyboard accessibility for star rating |
| `static/css/style.css` | Modified — focus-visible style for star rating |

---

## Live Demo

**https://mediguide-ezpe.onrender.com**
