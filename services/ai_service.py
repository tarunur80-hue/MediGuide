# services/ai_service.py
#
# WHAT THIS FILE DOES:
# Takes a user's symptom description and returns a structured assessment:
# condition, reasoning, severity, an OTC suggestion (if mild) or specialist
# type (if serious), and a safety disclaimer.
#
# ------------------------------------------------------------------
# IMPORTANT - CURRENT STATUS: PLACEHOLDER MODE (no real AI call yet)
# ------------------------------------------------------------------
# We are not calling the real Claude API yet because it requires paid
# credits, and that decision was deliberately paused today. Instead,
# analyze_symptoms() below uses simple keyword-matching rules to return
# realistic, structured responses -- with the EXACT SAME return shape
# the real Claude-powered version will use.
#
# WHEN YOU'RE READY TO SWITCH TO THE REAL CLAUDE API:
# Only the code INSIDE analyze_symptoms() needs to change. Every route,
# template, and piece of code that CALLS this function stays exactly
# the same, because the function signature and return dictionary shape
# will not change. The real version is included below (commented out)
# as a ready-to-use reference for that swap.

import re


def analyze_symptoms(symptom_text: str) -> dict:
    """
    Analyzes free-text symptoms and returns a structured result.

    Returns a dict with keys:
        condition (str)
        reasoning (str)
        severity (str) -- "mild" or "uncertain-serious"
        otc_suggestion (str or None)
        specialist_type (str or None)
        disclaimer (str)
    """
    text = symptom_text.lower()

    # --- Simple rule-based keyword matching (placeholder logic) ---
    serious_keywords = [
        "chest pain", "chest tightness", "difficulty breathing",
        "shortness of breath", "severe bleeding", "unconscious",
        "seizure", "blue lips", "confusion", "slurred speech",
        "one side weak", "severe headache", "suicidal"
    ]
    mild_cold_keywords = ["cold", "sore throat", "runny nose", "sneezing", "mild fever", "cough"]
    headache_keywords = ["headache", "migraine"]
    stomach_keywords = ["stomach", "nausea", "vomit", "diarrhea", "indigestion"]

    disclaimer = (
        "This is not a medical diagnosis. Please consult a doctor for confirmation, "
        "especially if symptoms are severe, persistent, or worsening."
    )

    # Check for anything that sounds serious first (safety-first ordering)
    if any(keyword in text for keyword in serious_keywords):
        return {
            "condition": "Symptoms that may require urgent attention",
            "reasoning": (
                "You've described symptoms that can sometimes be associated with serious "
                "underlying conditions. Without an in-person examination, it isn't possible "
                "to rule out anything serious, so we recommend seeing a doctor promptly."
            ),
            "severity": "uncertain-serious",
            "otc_suggestion": None,
            "specialist_type": "General Physician (or Emergency Care if symptoms are severe)",
            "disclaimer": disclaimer,
        }

    if any(keyword in text for keyword in mild_cold_keywords):
        return {
            "condition": "Common Cold",
            "reasoning": (
                "Symptoms like a sore throat, runny nose, sneezing, or mild fever are "
                "commonly associated with a common cold, which is usually a mild, "
                "self-resolving viral infection."
            ),
            "severity": "mild",
            "otc_suggestion": "Paracetamol for fever/discomfort, warm fluids, and rest. "
                               "See a doctor if symptoms last more than 7-10 days or worsen.",
            "specialist_type": None,
            "disclaimer": disclaimer,
        }

    if any(keyword in text for keyword in headache_keywords):
        return {
            "condition": "Tension Headache",
            "reasoning": (
                "Headaches described without other serious warning signs are often "
                "tension-type headaches, commonly linked to stress, screen time, or dehydration."
            ),
            "severity": "mild",
            "otc_suggestion": "Paracetamol or ibuprofen, hydration, and rest in a quiet, dim room. "
                               "See a doctor if headaches are severe, sudden, or recurring frequently.",
            "specialist_type": None,
            "disclaimer": disclaimer,
        }

    if any(keyword in text for keyword in stomach_keywords):
        return {
            "condition": "Mild Digestive Upset",
            "reasoning": (
                "Symptoms like nausea, mild stomach discomfort, or occasional diarrhea are "
                "often linked to minor digestive upset or mild food intolerance."
            ),
            "severity": "mild",
            "otc_suggestion": "Oral rehydration solution, bland diet (like rice/toast), and rest. "
                               "See a doctor if symptoms persist beyond 2 days or include blood or high fever.",
            "specialist_type": None,
            "disclaimer": disclaimer,
        }

    # Default fallback: nothing matched confidently -> be cautious
    return {
        "condition": "Unable to determine a clear pattern",
        "reasoning": (
            "The symptoms described don't clearly match a common, well-understood pattern. "
            "Because we can't be confident about what's causing this, the safest next step "
            "is a proper in-person evaluation."
        ),
        "severity": "uncertain-serious",
        "otc_suggestion": None,
        "specialist_type": "General Physician",
        "disclaimer": disclaimer,
    }


# ------------------------------------------------------------------
# REFERENCE: Real Claude API version (use this once credits are added)
# ------------------------------------------------------------------
# import os
# import json
# from anthropic import Anthropic
#
# client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
#
# SYSTEM_PROMPT = """You are a cautious medical triage assistant. Given a
# user's described symptoms, respond with ONLY valid JSON (no markdown, no
# extra text) with these exact keys: condition, reasoning, severity
# ("mild" or "uncertain-serious"), otc_suggestion (string or null),
# specialist_type (string or null), disclaimer (string).
# Be reasonably confident for clearly mild, common cases (like a common
# cold), but default to "uncertain-serious" and recommend a specialist
# whenever symptoms are ambiguous, severe, or could indicate something
# serious. Never give prescription-strength dosage instructions - only
# general OTC category suggestions. Always include a disclaimer stating
# this is not a medical diagnosis."""
#
# def analyze_symptoms(symptom_text: str) -> dict:
#     try:
#         response = client.messages.create(
#             model="claude-sonnet-4-6",
#             max_tokens=500,
#             temperature=0.3,
#             system=SYSTEM_PROMPT,
#             messages=[{"role": "user", "content": symptom_text}],
#         )
#         raw_text = response.content[0].text.strip()
#         raw_text = raw_text.replace("```json", "").replace("```", "").strip()
#         return json.loads(raw_text)
#     except Exception:
#         return {
#             "condition": "We couldn't analyze this right now",
#             "reasoning": "There was a problem reaching our AI service. Please try again in a moment.",
#             "severity": "uncertain-serious",
#             "otc_suggestion": None,
#             "specialist_type": "General Physician",
#             "disclaimer": "This is not a medical diagnosis. Please consult a doctor for confirmation.",
#         }
