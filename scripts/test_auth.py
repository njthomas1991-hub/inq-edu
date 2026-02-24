import os
import sys
import django
from django.contrib.auth import get_user_model, authenticate

# Ensure project root is on sys.path so Django settings package can be imported
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inclusive_quest_education.settings')
django.setup()

User = get_user_model()
print('Total users:', User.objects.count())
last = User.objects.order_by('-id').first()
if last:
    print('Last user id,username,email,has_usable_password:', last.id, last.username, last.email, last.has_usable_password())
else:
    print('No users yet')

# Create a fresh test user
base = 'authtest'
username = base
suffix = 1
while User.objects.filter(username=username).exists():
    username = f"{base}{suffix}"
    suffix += 1
pw = 'TestPass123!'
user = User.objects.create_user(username=username, email=f'{username}@example.com', password=pw)
print('Created test user:', user.username)

# Try authenticate by username
auth = authenticate(username=username, password=pw)
print('Authenticate by username returned:', auth and auth.username)

# Try authenticate by email (simulate CustomAuthenticationForm mapping)
auth2 = None
try:
    u = User.objects.get(email__iexact=f'{username}@example.com')
    auth2 = authenticate(username=u.username, password=pw)
except Exception as e:
    print('Email lookup failed:', e)
print('Authenticate by email lookup returned:', auth2 and auth2.username)
