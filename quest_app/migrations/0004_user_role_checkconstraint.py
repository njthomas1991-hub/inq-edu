from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quest_app", "0003_class_level_class_subject"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                condition=(
                    models.Q(role__in=["student", "teacher", "school_admin"]) |
                    models.Q(role__isnull=True)
                ),
                name="user_role_valid",
            ),
        ),
    ]
