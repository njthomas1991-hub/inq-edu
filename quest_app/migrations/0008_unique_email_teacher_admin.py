"""Make teacher/school_admin emails unique by removing duplicates then adding DB constraint.

This migration:
 - Finds duplicate non-null emails among users with role in (teacher, school_admin).
   For each duplicate group, it keeps the lowest-PK user email and sets other users' email to NULL.
 - Adds a conditional UniqueConstraint on `email` for teacher/school_admin users.
"""

from django.db import migrations, models


def dedupe_teacher_admin_emails(apps, schema_editor):
    User = apps.get_model("quest_app", "User")
    # Collect emails -> list of users
    groups = {}
    for u in (
        User.objects.filter(email__isnull=False)
        .filter(role__in=["teacher", "school_admin"])
        .order_by("id")
    ):
        groups.setdefault(u.email.lower(), []).append(u)

    for email, users in groups.items():
        if len(users) <= 1:
            continue
        # keep the first (lowest id), nullify the rest
        keeper = users[0]
        for dupe in users[1:]:
            dupe.email = None
            dupe.save(update_fields=["email"])


class Migration(migrations.Migration):

    dependencies = [
        ("quest_app", "0007_populate_timestamps_nonnull"),
    ]

    operations = [
        migrations.RunPython(
            dedupe_teacher_admin_emails, reverse_code=migrations.RunPython.noop
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(role__in=["teacher", "school_admin"]),
                name="unique_email_teacher_admin",
            ),
        ),
    ]
