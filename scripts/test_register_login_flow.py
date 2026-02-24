import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inclusive_quest_education.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

c = Client()
email = 'flowtest@example.com'
username_base = email.split('@',1)[0]
first='Flow'
last='Test'
role='teacher'
password='FlowPass123!'

print('Starting flow test: register -> logout -> login')
# Ensure no leftover user
User.objects.filter(email__iexact=email).delete()

# Register
server_kwargs = {'HTTP_HOST': 'localhost'}
resp = c.post('/register/', {
    'email': email,
    'first_name': first,
    'last_name': last,
    'role': role,
    'password1': password,
    'password2': password,
    'remember_me': 'on'
}, **server_kwargs)
print('Register POST status:', resp.status_code)
# After register, check if user created
user = User.objects.filter(email__iexact=email).first()
print('User created:', bool(user), getattr(user, 'username', None))
if user:
    print('has_usable_password():', user.has_usable_password())

# Ensure logged in
session_user = None
if '_auth_user_id' in c.session:
    session_user = c.session.get('_auth_user_id')
print('Session _auth_user_id after register:', session_user)

# Logout
resp = c.get('/logout/', **server_kwargs)
print('Logout GET status:', resp.status_code)
print('Session keys after logout:', list(c.session.keys()))

# Attempt login using email
resp = c.post('/login/', {'username': email, 'password': password, 'remember': 'on'}, **server_kwargs)
print('Login POST status with email:', resp.status_code)
print('Login POST redirect chain:', getattr(resp, 'url', None))
print('Login response content snippet:', resp.content[:500])
print('Session _auth_user_id after login attempt:', c.session.get('_auth_user_id'))

# Attempt login using username
if user:
    resp2 = c.post('/login/', {'username': user.username, 'password': password, 'remember': 'on'}, **server_kwargs)
    print('Login POST status with username:', resp2.status_code)
    print('Session _auth_user_id after username login attempt:', c.session.get('_auth_user_id'))

print('Users total:', User.objects.count())
