import os
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_portfolio.settings')
django.setup()

from accounts.models import StudentRegistry

# Student data to insert
data = [
    {
        "matric_number": "FST/20/001",
        "first_name": "David",
        "middle_name": "Tunde",
        "last_name": "Adesina",
        "date_of_birth": date(2000, 3, 15),
        "faculty": "Science",
        "department": "Computer Science",
        "level": "400",
    },
    {
        "matric_number": "FST/20/002",
        "first_name": "Amina",
        "middle_name": "",
        "last_name": "Bello",
        "date_of_birth": date(1999, 11, 22),
        "faculty": "Science",
        "department": "Biochemistry",
        "level": "400",
    },
    {
        "matric_number": "FST/20/003",
        "first_name": "John",
        "middle_name": "Ike",
        "last_name": "Okoro",
        "date_of_birth": date(2001, 7, 9),
        "faculty": "Engineering",
        "department": "Mechanical Engineering",
        "level": "500",
    },
    {
        "matric_number": "FST/20/004",
        "first_name": "Chioma",
        "middle_name": "Nkechi",
        "last_name": "Nwankwo",
        "date_of_birth": date(2000, 1, 5),
        "faculty": "Health Sciences",
        "department": "Nursing",
        "level": "400",
    },
    {
        "matric_number": "FST/20/005",
        "first_name": "Samuel",
        "middle_name": "Kunle",
        "last_name": "Adebayo",
        "date_of_birth": date(1998, 6, 30),
        "faculty": "Social Sciences",
        "department": "Psychology",
        "level": "400",
    },
    {
        "matric_number": "FST/20/006",
        "first_name": "Fatima",
        "middle_name": "Yusuf",
        "last_name": "Aliyu",
        "date_of_birth": date(1999, 12, 1),
        "faculty": "Law",
        "department": "Public Law",
        "level": "500",
    },
    {
        "matric_number": "FST/20/007",
        "first_name": "Emeka",
        "middle_name": "",
        "last_name": "Eze",
        "date_of_birth": date(2000, 4, 18),
        "faculty": "Engineering",
        "department": "Electrical Engineering",
        "level": "500",
    },
    {
        "matric_number": "FST/20/008",
        "first_name": "Zainab",
        "middle_name": "K.",
        "last_name": "Mohammed",
        "date_of_birth": date(2001, 8, 25),
        "faculty": "Science",
        "department": "Microbiology",
        "level": "400",
    },
    {
        "matric_number": "FST/20/009",
        "first_name": "Tomiwa",
        "middle_name": "Dare",
        "last_name": "Ogunleye",
        "date_of_birth": date(1998, 9, 10),
        "faculty": "Arts",
        "department": "English",
        "level": "400",
    },
    {
        "matric_number": "FST/20/010",
        "first_name": "Blessing",
        "middle_name": "",
        "last_name": "Etim",
        "date_of_birth": date(2000, 5, 12),
        "faculty": "Management Sciences",
        "department": "Accounting",
        "level": "400",
    }
]

# Insert data
for student in data:
    obj, created = StudentRegistry.objects.get_or_create(**student)
    print(f"{'Created' if created else 'Exists'}: {obj}")
