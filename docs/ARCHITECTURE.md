# MediGuide — System Architecture

Version 1.0 | Day 2 Deliverable | AB Talks 60-Day Claude Challenge Capstone

---

## 1. Tech Stack (Finalized)

| Layer | Choice | Reasoning |
|---|---|---|
| Backend | Python + Flask | Matches strongest skill (Python); lightweight, minimal boilerplate, ideal for a 10-day solo build |
| Frontend | HTML + CSS + JavaScript (Jinja2 templates) | No build step, no framework overhead, fastest path to a working UI |
| Database | SQLite + Flask-SQLAlchemy | Zero-config, file-based, free; ORM avoids raw SQL and speeds up development |
| Authentication | Flask-Login + Werkzeug (hashed PIN) | Secure, standard session handling without custom crypto code |
| AI Model | Claude API (Anthropic) via official `anthropic` Python SDK | Real reasoning-based symptom analysis, as scoped in PRD |
| Hosting | Render.com (free web service tier) | Free, GitHub-connected auto-deploy, supports Flask + gunicorn |
| Other Tools | python-dotenv, gunicorn, Git/GitHub | Standard, free, low-friction tooling |

---

## 2. Component Diagram

```mermaid
graph TB
    subgraph Client["Client (Browser)"]
        UI[HTML/CSS/JS Pages]
    end

    subgraph Server["Flask Application (app.py)"]
        Routes[Route Handlers]
        Auth[Auth Module - Flask-Login]
        AIService[AI Service - services/ai_service.py]
        DoctorRepo[Doctor Repository - data/doctor_repository.py]
        Models[SQLAlchemy Models - User, Booking, Review]
    end

    subgraph Data["Data Layer"]
        SQLite[(SQLite DB - mediguide.db)]
        MockJSON[[Mock JSON - data/doctors.json]]
    end

    subgraph External["External Services"]
        ClaudeAPI[Claude API - Anthropic]
    end

    UI -->|HTTP Request| Routes
    Routes --> Auth
    Routes --> AIService
    Routes --> DoctorRepo
    Routes --> Models
    Auth --> Models
    Models --> SQLite
    DoctorRepo --> MockJSON
    AIService -->|API Call| ClaudeAPI
    ClaudeAPI -->|JSON Response| AIService
    Routes -->|HTML Response| UI
```

---

## 3. Data Flow — Symptom Checker

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Flask Route (/symptom-checker)
    participant S as ai_service.py
    participant C as Claude API

    U->>F: POST symptom text
    F->>S: analyze_symptoms(text)
    S->>C: messages.create() with system prompt
    C-->>S: JSON: condition, reasoning, severity, suggestion, disclaimer
    S-->>F: Parsed Python dict
    F-->>U: Render results.html with structured data
```

---

## 4. Data Flow — Appointment Booking (Login-Gated)

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant F as Flask Route
    participant L as Flask-Login
    participant DB as SQLite (Booking table)
    participant J as doctors.json

    U->>F: GET /doctors/<id>/book
    F->>L: current_user.is_authenticated?
    alt Not logged in
        F-->>U: Redirect to /login?next=...
    else Logged in
        F->>J: Load doctor info by id
        F-->>U: Render booking form
        U->>F: POST booking (date, time_slot)
        F->>DB: INSERT Booking (user_id, doctor_id, date, time_slot)
        DB-->>F: Confirmation
        F-->>U: Redirect to /my-appointments
    end
```

---

## 5. Request Lifecycle (General Pattern)

```mermaid
flowchart LR
    A[Browser Request] --> B{Route Matches?}
    B -->|No| C[404 Page]
    B -->|Yes| D{Requires Login?}
    D -->|Yes, not logged in| E[Redirect to /login]
    D -->|No or Logged in| F[Route Handler Executes]
    F --> G{Needs DB?}
    F --> H{Needs Mock JSON?}
    F --> I{Needs AI Call?}
    G -->|Yes| J[SQLAlchemy Query]
    H -->|Yes| K[Read doctors.json]
    I -->|Yes| L[Claude API Call]
    J --> M[Render Template]
    K --> M
    L --> M
    M --> N[HTML Response to Browser]
```

---

## 6. AI Interaction Detail

- **Trigger:** User submits free-text symptoms via `/symptom-checker` (POST).
- **Prompt design:** System prompt instructs Claude to respond in strict JSON only, with fields: `condition`, `reasoning`, `severity` (`mild` | `uncertain-serious`), `otc_suggestion` (nullable), `specialist_type` (nullable), `disclaimer`.
- **Safety behavior:** Claude is instructed to be reasonably confident for clearly mild cases, but default to `uncertain-serious` + specialist recommendation whenever symptoms are ambiguous.
- **Failure handling:** If the API call fails or returns invalid JSON, the app shows a graceful fallback message rather than crashing (wrapped in try/except).
- **No conversation memory:** Each symptom check is a single, stateless API call — no chat history is stored or sent.

---

## 7. External Services

| Service | Purpose | Failure Handling |
|---|---|---|
| Claude API (Anthropic) | Symptom analysis | Try/except wrapper; user sees a friendly error message and can retry |
| Render.com | Hosting | N/A (infrastructure, not runtime-dependent) |

No other external services are used in v1.0 (no maps API, no SMS/OTP API, no payment gateway) — consistent with PRD's explicit exclusions.
