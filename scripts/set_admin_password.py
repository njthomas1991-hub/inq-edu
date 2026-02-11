import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from core.models import User

user = User.objects.get(username='admin')
user.set_password('Admin@123')
user.save()
print("Admin password set to: Admin@123")
