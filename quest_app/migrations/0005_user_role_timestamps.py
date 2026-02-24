"""Make `role` non-nullable (default 'student') and add timestamp fields.

This migration:
 - Sets any existing NULL/empty `role` values to 'student'.
 - Adds `created_at`/`updated_at` to `User` and `Class` and `updated_at` to TeachingResource.

Model-level validation enforces unique teacher/admin emails; a DB-level conditional
unique constraint is intentionally not added here for compatibility across DBs.
"""

from django.db import migrations, models


def set_default_roles(apps, schema_editor):
    User = apps.get_model("quest_app", "User")
    for u in User.objects.filter(role__isnull=True):
        u.role = "student"
        u.save(update_fields=["role"])


class Migration(migrations.Migration):

    dependencies = [
        ("quest_app", "0004_user_role_checkconstraint"),
    ]

    operations = [
        migrations.RunPython(set_default_roles, reverse_code=migrations.RunPython.noop),
        migrations.AddField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="class",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="class",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="teachingresource",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("student", "Student"),
                    ("teacher", "Teacher"),
                    ("school_admin", "School Admin"),
                ],
                default="student",
                max_length=20,
            ),
        ),
    ]
