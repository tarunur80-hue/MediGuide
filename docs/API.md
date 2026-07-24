# MediGuide — API Design

Version 1.0 | Day 2 Deliverable

All endpoints are served by the Flask app. This is a server-rendered app (Jinja2 templates), so most "responses" are HTML pages, not JSON — except where noted. No implementation yet; this is the full contract for Day 3+ builds.

---

## Authentication Endpoints

### `GET /signup`
- **Purpose:** Show signup form
- **Auth:** Public
- **Response:** HTML form (phone_number, pin, confirm_pin)

### `POST /signup`
- **Purpose:** Create a new user account
- **Request (form):** `phone_number` (string, 10 digits), `pin` (4-6 digits), `confirm_pin`
- **Validation:**
  - phone_number: exactly 10 digits, numeric only, not already registered
  - pin: 4-6 digits, numeric only
  - pin === confirm_pin
- **Response:** Redirect to `/` (auto-logged in) on success; re-render form with flash error on failure
- **Auth:** Public
- **Error cases:** Duplicate phone number → "Phone number already registered"; PIN mismatch → "PINs do not match"; invalid format → "Enter a valid 10-digit phone number"

### `GET /login`
- **Purpose:** Show login form
- **Auth:** Public
- **Response:** HTML form (phone_number, pin)

### `POST /login`
- **Purpose:** Authenticate existing user
- **Request (form):** `phone_number`, `pin`
- **Validation:** phone_number exists, pin matches stored hash
- **Response:** Redirect to `next` param or `/` on success; re-render with flash error on failure
- **Auth:** Public
- **Error cases:** Unknown phone number or wrong PIN → generic "Invalid phone number or PIN" (never reveal which field is wrong, for security)

### `POST /logout`
- **Purpose:** End user session
- **Auth:** Logged-in users only
- **Response:** Redirect to `/`

---

## Symptom Checker Endpoints

### `GET /symptom-checker`
- **Purpose:** Show symptom input form
- **Auth:** Public
- **Response:** HTML form (free-text textarea)

### `POST /symptom-checker`
- **Purpose:** Submit symptoms, get AI-generated assessment
- **Request (form):** `symptoms` (string, min 3 characters)
- **Validation:** Non-empty, reasonable length cap (e.g., max 1000 characters) to avoid abuse
- **Response:** Renders `results.html` with: condition, reasoning, severity, otc_suggestion or specialist_type, disclaimer
- **Auth:** Public
- **Error cases:** Empty input → flash "Please describe your symptoms"; Claude API failure → render a friendly fallback message ("We couldn't analyze this right now, please try again"); malformed AI JSON → same fallback

---

## Doctor Directory Endpoints

### `GET /doctors`
- **Purpose:** Browse/filter doctor & hospital directory
- **Query params (optional):** `specialty`, `area`
- **Auth:** Public
- **Response:** HTML card grid of matching doctors; empty-state message if no matches
- **Error cases:** Invalid/unknown filter value → simply returns empty results, no error thrown

### `GET /doctors/<doctor_id>`
- **Purpose:** View full doctor detail page (bio, reviews, booking button)
- **Auth:** Public
- **Response:** HTML detail page
- **Error cases:** Unknown `doctor_id` → 404 page

---

## Booking Endpoints

### `GET /doctors/<doctor_id>/book`
- **Purpose:** Show appointment booking form for a specific doctor
- **Auth:** Login required (redirect to `/login?next=...` if not authenticated)
- **Response:** HTML form (date picker, time slot dropdown)
- **Error cases:** Unknown `doctor_id` → 404

### `POST /doctors/<doctor_id>/book`
- **Purpose:** Create a new booking
- **Request (form):** `appointment_date` (date), `time_slot` (string)
- **Validation:** date must be today or future; time_slot must be one of the predefined mock slots
- **Auth:** Login required
- **Response:** Redirect to `/my-appointments` with success flash message
- **Error cases:** Past date selected → "Please choose a future date"; invalid time slot → "Please select a valid time slot"

### `GET /my-appointments`
- **Purpose:** List all bookings belonging to the logged-in user
- **Auth:** Login required
- **Response:** HTML list/table of bookings with status badges and action buttons

### `GET /appointments/<booking_id>/reschedule`
- **Purpose:** Show reschedule form pre-filled with current date/time
- **Auth:** Login required + ownership check (`booking.user_id == current_user.id`)
- **Response:** HTML form
- **Error cases:** Booking belongs to another user → 403 Forbidden; unknown booking_id → 404

### `POST /appointments/<booking_id>/reschedule`
- **Purpose:** Update booking date/time
- **Request (form):** `appointment_date`, `time_slot`
- **Validation:** Same as booking creation
- **Auth:** Login required + ownership check
- **Response:** Redirect to `/my-appointments` with success flash

### `POST /appointments/<booking_id>/cancel`
- **Purpose:** Cancel an existing booking
- **Auth:** Login required + ownership check
- **Response:** Redirect to `/my-appointments`, booking status updated to "cancelled"
- **Error cases:** Already cancelled → flash "This appointment is already cancelled"; not owner → 403

---

## Review Endpoints

### `POST /doctors/<doctor_id>/review`
- **Purpose:** Submit a new review/rating for a doctor
- **Request (form):** `rating` (int, 1-5), `text` (string, non-empty)
- **Validation:** rating in range 1-5; text not empty; doctor_id exists in doctors.json
- **Auth:** Login required
- **Response:** Redirect to `/doctors/<doctor_id>` with new review visible
- **Error cases:** Invalid rating → "Please select a rating between 1 and 5"; empty text → "Please write a short review"; not logged in → redirect to login

---

## Error / Utility Routes

### `GET /404` (auto-triggered)
- **Purpose:** Friendly not-found page for unknown routes or missing resources
- **Auth:** Public

### `GET /500` (auto-triggered)
- **Purpose:** Friendly generic error page for unexpected server errors
- **Auth:** Public

---

## Summary Table

| Method | Route | Auth Required | Purpose |
|---|---|---|---|
| GET/POST | /signup | Public | Create account |
| GET/POST | /login | Public | Authenticate |
| POST | /logout | Logged in | End session |
| GET/POST | /symptom-checker | Public | AI symptom analysis |
| GET | /doctors | Public | Browse/filter directory |
| GET | /doctors/<id> | Public | Doctor detail + reviews |
| GET/POST | /doctors/<id>/book | Logged in | Create booking |
| GET | /my-appointments | Logged in | List own bookings |
| GET/POST | /appointments/<id>/reschedule | Logged in + owner | Update booking |
| POST | /appointments/<id>/cancel | Logged in + owner | Cancel booking |
| POST | /doctors/<id>/review | Logged in | Submit review |
