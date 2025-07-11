import os
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_portfolio.settings')
django.setup()

from accounts.models import NINDatabase, StudentRegistry
from portfolio.models import Skill

# ---------- Insert NIN Data ----------
print("=== Processing NIN data ===")

try:
    with open('clients.json') as f:
        nin_data = json.load(f)
except FileNotFoundError:
    print("❌ nin_data.json file not found. Skipping NIN data import.")
    nin_data = []

for person in nin_data:
    nin = person["nin"]
    first_name = person["first_name"]
    middle_name = person.get("middle_name", "")
    last_name = person["last_name"]
    date_of_birth = datetime.strptime(person["date_of_birth"], "%Y-%m-%d").date()

    obj, created = NINDatabase.objects.get_or_create(
        nin=nin,
        defaults={
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
        }
    )
    print(f"{'✅ Created' if created else '⚠️ Exists'} NIN: {obj}")

print("✅ Finished processing NIN data.\n")

# ---------- Insert Student Data ----------
print("=== Processing student registry data ===")

try:
    with open('students.json') as f:
        students_json = json.load(f)
        students_data = students_json["students"]
except FileNotFoundError:
    print("❌ students.json file not found. Skipping student data import.")
    students_data = []

for student in students_data:
    matric_number = student["matric_number"]
    first_name = student["first_name"]
    middle_name = student.get("middle_name", "")
    last_name = student["last_name"]
    faculty = student["faculty"]
    department = student["department"]
    date_of_birth = datetime.strptime(student["dob"], "%Y-%m-%d").date()
    year_of_entry = str(student["year_of_entry"])
    level = str(student["level"])

    obj, created = StudentRegistry.objects.get_or_create(
        matric_number=matric_number,
        defaults={
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "faculty": faculty,
            "department": department,
            "year_of_entry": year_of_entry,
            "level": level,
        }
    )
    print(f"{'✅ Created' if created else '⚠️ Exists'} Student: {obj}")

print("✅ Finished processing student data.\n")

# ---------- Insert Skills Data ----------
print("=== Processing skills data ===")

try:
    with open('skills.json') as f:
        skills_json = json.load(f)  # This is a list of dicts
except FileNotFoundError:
    print("❌ skills.json file not found. Skipping skills data import.")
    skills_json = []

for skill in skills_json:
    skill_name = skill.get("name", "").strip()
    if skill_name:
        obj, created = Skill.objects.get_or_create(name=skill_name)
        print(f"{'✅ Created' if created else '⚠️ Exists'} Skill: {obj}")

print("✅ Finished processing skills data.\n")
