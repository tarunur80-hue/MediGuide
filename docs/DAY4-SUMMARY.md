# MediGuide — Day 4 Summary

Core Feature Implementation: AI Symptom Checker | AB Talks 60-Day Claude Challenge Capstone

---

## ✅ What Was Completed Today

1. **Symptom Checker feature built end-to-end**
   - `/symptom-checker` route (GET shows form, POST analyzes and shows results)
   - Input validation: minimum 3 characters, maximum 1000 characters
   - Flash messaging for validation errors, redirecting back to the form

2. **AI service layer created** (`services/ai_service.py`)
   - `analyze_symptoms()` function with a fixed, stable interface:
     returns `condition`, `reasoning`, `severity`, `otc_suggestion`,
     `specialist_type`, `disclaimer`
   - Currently running in **placeholder mode** using rule-based keyword
     matching (see decision note below)
   - Real Claude API version written and included as ready-to-activate
     reference code in the same file — swapping it in later requires no
     changes anywhere else in the app

3. **UI built for both states**
   - `templates/symptom_checker.html` — input form with loading state
   - `templates/results.html` — displays condition, reasoning, OTC suggestion
     or specialist recommendation, and a mandatory disclaimer box
   - Severity-based visual treatment: green "MILD" badge vs. orange
     "NEEDS ATTENTION" badge

4. **Navigation wired**
   - "Symptom Checker" navbar link now points to the real route
   - "Find Doctors" and "Login" remain placeholders (Day 5+ as scheduled)

5. **Verified working**
   - Mild case (cold symptoms) → correct OTC-suggestion result
   - Serious case (chest pain/breathing difficulty) → correct specialist
     recommendation, no OTC suggestion shown
   - Ambiguous/unmatched input → safely defaults to "see a doctor" rather
     than guessing — confirms the safety-first fallback behavior works

---

## ⚠️ Important Decision Made Today: AI Running in Placeholder Mode

**What happened:** Setting up the real Claude API required adding paid
credits to the Anthropic Console (there is no free tier for the API).
After discussing options (add credits vs. switch providers vs. pause),
the decision was to **pause the real API integration** for now and build
the full feature with a realistic placeholder so today's milestone could
still be completed on schedule.

**What this means technically:** `analyze_symptoms()` currently uses
keyword-matching rules instead of a real Claude API call. The function's
inputs and outputs are identical to what the real version will use, so:
- No other file in the app needs to change when the real API is activated
- The real Claude API code is already written and included (commented out)
  directly inside `services/ai_service.py`, ready to uncomment and use

**What's needed to activate the real AI:**
1. Add credits to the Anthropic Console (console.anthropic.com → Billing)
2. Generate an API key and add it to `.env` as `ANTHROPIC_API_KEY`
3. Swap the placeholder function body for the commented-out real version
   in `services/ai_service.py`
4. No route, template, or other file changes are required

This is a deliberate, reversible scope decision — not a shortcut that
compromises the final product. The PRD and Blueprint still call for the
real Claude API in the finished v1.0, and this remains fully achievable
before Day 10.

---

## 🚧 What's Ready to Build Tomorrow (Day 5)

- The results page already includes a "Find a Doctor Nearby" button
  (currently disabled/marked "coming soon") — this becomes fully
  functional once the doctor directory exists
- Homepage and navbar are ready for the "Find Doctors" link to go live
- No blockers going into Day 5

---

## 🎯 Tomorrow's Objective

Build the **Doctor & Hospital Directory** (hero feature): create the mock
dataset (20-30 doctors/hospitals), the repository/query helper, and the
public browsing + filtering UI — exactly as scoped in the PRD and Blueprint.

---

## Files Changed/Added Today

| File | Status |
|---|---|
| `app.py` | Modified — added `/symptom-checker` route |
| `services/__init__.py` | New |
| `services/ai_service.py` | New |
| `templates/symptom_checker.html` | New |
| `templates/results.html` | New |
| `templates/base.html` | Modified — wired Symptom Checker nav link |
| `static/css/style.css` | Modified — added form, results, badge, disclaimer styles |
