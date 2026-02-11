#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from core.models import User

# Check for existing superusers
superusers = User.objects.filter(is_superuser=True)
print(f"Found {superusers.count()} superuser(s):")
for user in superusers:
    print(f"  - Username: {user.username}, Email: {user.email}, Role: {user.role}")

# If no superusers exist, offer to create one
if superusers.count() == 0:
    print("\nNo superusers found. You can create one with:")
    print("python backend/manage.py createsuperuser")
