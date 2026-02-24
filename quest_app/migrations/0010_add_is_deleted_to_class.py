from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quest_app", "0009_delete_duplicate_teacher_admin_accounts"),
    ]

    operations = [
        migrations.AddField(
            model_name="class",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
