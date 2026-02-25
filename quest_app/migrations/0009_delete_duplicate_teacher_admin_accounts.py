"""Delete duplicate teacher/school_admin user accounts keeping the lowest-PK.

This migration finds users with the same email (case-insensitive) who have
role in ('teacher', 'school_admin') and deletes every user except the one
with the lowest primary key for that email.
"""

from django.db import migrations


def delete_duplicate_accounts(apps, schema_editor):
    User = apps.get_model("quest_app", "User")
    # Collect emails -> ordered list of users
    groups = {}
    for u in (
        User.objects.filter(email__isnull=False)
        .filter(role__in=["teacher", "school_admin"])
        .order_by("id")
    ):
        groups.setdefault(u.email.lower(), []).append(u)

    to_delete_ids = []
    for email, users in groups.items():
        if len(users) <= 1:
            continue
        # keep first (lowest id), delete the rest
        for dupe in users[1:]:
            to_delete_ids.append(dupe.id)

    if to_delete_ids:
        User.objects.filter(id__in=to_delete_ids).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("quest_app", "0008_unique_email_teacher_admin"),
    ]

    operations = [
        migrations.RunPython(
            delete_duplicate_accounts, reverse_code=migrations.RunPython.noop
        ),
    ]
