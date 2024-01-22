import datetime
import os
import random

import django
import names
from django.utils import timezone

# Reset database - WARNING: This will erase your data
os.system("echo 'yes' | python manage.py reset_db")
os.system("python manage.py migrate")

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_lessons.settings")
django.setup()

from employees_management.models import (
    Assignment,
    Department,
    Employee,
    EmployeeStatus,
    Profile,
)


def random_date_in_last_12_months():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return timezone.make_aware(start_date + datetime.timedelta(days=random_number_of_days))


def random_date_of_birth():
    end_date = datetime.datetime.now() - datetime.timedelta(days=20 * 365)
    start_date = end_date - datetime.timedelta(days=30 * 365)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return timezone.make_aware(start_date + datetime.timedelta(days=random_number_of_days))


departments = ["HR", "Finance", "Development", "Sales", "Support"]
department_counts = [5, 8, 10, 12, 14]

for dept_name in departments:
    Department.objects.create(name=dept_name)

for index, department in enumerate(departments):
    dept_instance = Department.objects.get(name=department)

    for _ in range(department_counts[index]):
        profile = Profile.objects.create(date_of_birth=random_date_of_birth(), address="123, Some Street")

        emp = Employee.objects.create(
            name=names.get_full_name(),
            status=random.choice([EmployeeStatus.ACTIVE, EmployeeStatus.INACTIVE]),
            profile=profile,
        )

        joined_at = random_date_in_last_12_months()
        left_at = random_date_in_last_12_months()
        if joined_at > left_at:
            joined_at, left_at = left_at, joined_at

        Assignment.objects.create(
            employee=emp, department=dept_instance, joined_at=joined_at, left_at=left_at
        )

print("Database recreated and data added successfully!")
