import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inclusive_quest_education.settings')
import django
django.setup()

from django.contrib.auth import get_user_model

def show_user(email):
    User = get_user_model()
    try:
        user = User.objects.filter(email__iexact=email).first()
    except Exception as e:
        print('Query error:', e)
        return 2
    if not user:
        print('No user found for email:', email)
        return 1
    print('id:', user.id)
    print('username:', user.username)
    print('email:', repr(user.email))
    print('is_active:', bool(getattr(user, 'is_active', True)))
    print('has_usable_password:', user.has_usable_password())
    print('role:', getattr(user, 'role', None))
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: show_user.py email@example.com')
        sys.exit(2)
    sys.exit(show_user(sys.argv[1]))
