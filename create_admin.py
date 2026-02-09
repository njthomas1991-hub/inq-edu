#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from backend.core.models import User

# Create a superuser with default credentials
username = 'admin'
email = 'admin@example.com'
password = 'admin12345'

# Check if admin already exists
if User.objects.filter(username=username).exists():
    print(f"Admin user '{username}' already exists.")
    user = User.objects.get(username=username)
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Is Superuser: {user.is_superuser}")
else:
    # Create the superuser
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='teacher'  # Grant teacher role
    )
    print(f"✓ Superuser created successfully!")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Password: {password}")
    print(f"\nAccess Django Admin at: http://127.0.0.1:8000/admin/")
