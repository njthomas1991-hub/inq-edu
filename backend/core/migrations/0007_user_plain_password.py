# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_superuser_to_schoolanalyticsprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='plain_password',
            field=models.CharField(blank=True, help_text='Plain text password for display purposes (students only)', max_length=100, null=True),
        ),
    ]
