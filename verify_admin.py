#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

from core.models import User

# Check admin user details
admin = User.objects.filter(username='admin').first()
if admin:
    print("Admin User Details:")
    print(f"  Username: {admin.username}")
    print(f"  Email: {admin.email}")
    print(f"  Is Active: {admin.is_active}")
    print(f"  Is Staff: {admin.is_staff}")
    print(f"  Is Superuser: {admin.is_superuser}")
    print(f"  Role: {admin.role}")
    
    # Check if admin has any issues
    if not admin.is_active:
        print("\n✗ Admin is INACTIVE - activating...")
        admin.is_active = True
        admin.save()
        print("  ✓ Admin activated")
    
    if not admin.is_staff:
        print("\n✗ Admin is NOT STAFF - fixing...")
        admin.is_staff = True
        admin.save()
        print("  ✓ Staff status fixed")
    
    if not admin.is_superuser:
        print("\n✗ Admin is NOT SUPERUSER - fixing...")
        admin.is_superuser = True
        admin.save()
        print("  ✓ Superuser status fixed")
    
    print("\n✓ Admin user is ready to access admin site at: http://127.0.0.1:8000/admin/")
else:
    print("Admin user not found!")
