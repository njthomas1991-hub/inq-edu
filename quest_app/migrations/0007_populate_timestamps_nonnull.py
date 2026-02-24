"""Populate nullable timestamp fields and make them non-nullable.

This migration sets any NULL `created_at`/`updated_at` values to the current
time and then alters the fields to `null=False` so they are required.
"""

from django.db import migrations, models


def populate_timestamps(apps, schema_editor):
    from django.utils import timezone

    now = timezone.now()
    User = apps.get_model("quest_app", "User")
    Class = apps.get_model("quest_app", "Class")
    TeachingResource = apps.get_model("quest_app", "TeachingResource")

    User.objects.filter(created_at__isnull=True).update(created_at=now)
    User.objects.filter(updated_at__isnull=True).update(updated_at=now)
    Class.objects.filter(created_at__isnull=True).update(created_at=now)
    Class.objects.filter(updated_at__isnull=True).update(updated_at=now)
    TeachingResource.objects.filter(updated_at__isnull=True).update(updated_at=now)


class Migration(migrations.Migration):

    dependencies = [
        ("quest_app", "0006_alter_user_options_remove_user_user_role_valid"),
    ]

    operations = [
        migrations.RunPython(
            populate_timestamps, reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="class",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="class",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="teachingresource",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
