# Generated migration to rename class_obj to clazz

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_class_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classstudent',
            old_name='class_obj',
            new_name='clazz',
        ),
        migrations.AlterUniqueTogether(
            name='classstudent',
            unique_together={('student', 'clazz')},
        ),
    ]
