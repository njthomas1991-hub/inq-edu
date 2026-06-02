import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


def ensure_default_admin(apps, schema_editor):
    User = apps.get_model("core", "User")

    username = os.environ.get("ADMIN_USERNAME", "admin")
    email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    password = os.environ.get("ADMIN_PASSWORD", "admin12345")

    defaults = {
        "email": email,
        "is_staff": True,
        "is_superuser": True,
        "is_active": True,
        "role": "teacher",
    }

    user, created = User.objects.get_or_create(username=username, defaults=defaults)

    changed_fields = []
    for field, value in defaults.items():
        if getattr(user, field) != value:
            setattr(user, field, value)
            changed_fields.append(field)

    if created or not user.password:
        user.password = make_password(password)
        changed_fields.append("password")

    if created or changed_fields:
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_class_slug_and_more"),
    ]

    operations = [
        migrations.RunPython(ensure_default_admin, migrations.RunPython.noop),
    ]