#!/usr/bin/env python
"""Reset or create superuser with admin/Test123!"""

import os
import sys
from pathlib import Path

import django

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from core.models import User

username = "admin"
password = "Test123!"

user, created = User.objects.get_or_create(
    username=username,
    defaults={
        "is_staff": True,
        "is_superuser": True,
    },
)

if not created:
    # Update existing user to ensure superuser status
    user.is_staff = True
    user.is_superuser = True

# Set the password
user.set_password(password)
user.save()

if created:
    print(f"✓ Created superuser: {username}")
else:
    print(f"✓ Updated superuser: {username}")

print(f"  Password: {password}")
