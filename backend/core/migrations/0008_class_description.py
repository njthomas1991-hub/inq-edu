# Generated migration for adding description field to Class model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_user_plain_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
