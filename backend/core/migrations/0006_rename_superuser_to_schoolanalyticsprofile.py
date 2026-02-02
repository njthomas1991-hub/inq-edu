# Generated migration for renaming Superuser to SchoolAnalyticsProfile

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolAnalyticsProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.CharField(max_length=255)),
                ('can_access_all_teachers', models.BooleanField(default=True, help_text="Access all teachers' data in the same school")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.OneToOneField(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='analytics_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'School Analytics Profiles',
            },
        ),
        migrations.DeleteModel(
            name='Superuser',
        ),
    ]
