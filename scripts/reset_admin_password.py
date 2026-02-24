import os
import sys
import pathlib

# Make sure project root is on sys.path so Django settings import works
PROJECT_ROOT = str(pathlib.Path(__file__).resolve().parents[1])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Ensure settings are configured
os.environ.setdefault("DJANGO_SECRET_KEY", "dev-secret-for-local")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inclusive_quest_education.settings")

from django import setup
setup()

from quest_app.models import User

NEW_PASSWORD = "Rq7#v9K2pLm8!zY"

u = User.objects.filter(username="admin").first()
if not u:
    # Create a new superuser if one doesn't exist in this database
    from django.contrib.auth import get_user_model
    UserModel = get_user_model()
    u = UserModel.objects.create_superuser(username="admin", email="admin@example.com", password=NEW_PASSWORD)
    print("CREATED")

u.set_password(NEW_PASSWORD)
u.save()
print("PASSWORD_SET")
import os
import sys

# Ensure settings are configured
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inclusive_quest_education.settings")

from django import setup
setup()

from quest_app.models import User

NEW_PASSWORD = "Rq7#v9K2pLm8!zY"

u = User.objects.filter(username="admin").first()
if not u:
    print("NOTFOUND")
    sys.exit(2)

u.set_password(NEW_PASSWORD)
u.save()
print("PASSWORD_SET")
