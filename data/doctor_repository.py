# data/doctor_repository.py
#
# WHAT THIS FILE DOES:
# Loads the mock doctors.json file and provides simple functions to
# get all doctors, filter them by specialty/area, or fetch one by id.
# This keeps all "how do we read doctor data" logic in one place, so
# routes in app.py don't need to know the data lives in a JSON file.

import json
import os

_DATA_PATH = os.path.join(os.path.dirname(__file__), "doctors.json")
_cache = None


def _load_doctors():
    """Loads doctors.json once and caches it in memory for the app's lifetime."""
    global _cache
    if _cache is None:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def get_all_doctors():
    """Returns the full list of doctors/hospitals."""
    return _load_doctors()


def get_all_specialties():
    """Returns a sorted list of unique specialties, for building the filter dropdown."""
    doctors = _load_doctors()
    return sorted({d["specialty"] for d in doctors})


def get_all_areas():
    """Returns a sorted list of unique areas, for building the filter dropdown."""
    doctors = _load_doctors()
    return sorted({d["area"] for d in doctors})


def filter_doctors(specialty=None, area=None):
    """
    Returns doctors matching the given specialty and/or area.
    If a filter is None or empty string, that filter is ignored.
    """
    doctors = _load_doctors()

    if specialty:
        doctors = [d for d in doctors if d["specialty"] == specialty]

    if area:
        doctors = [d for d in doctors if d["area"] == area]

    return doctors


def get_doctor_by_id(doctor_id):
    """Returns a single doctor dict matching the given id, or None if not found."""
    doctors = _load_doctors()
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    return None
