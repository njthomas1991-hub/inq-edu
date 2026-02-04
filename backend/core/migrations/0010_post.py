# Generated migration to add Post model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_class_obj_to_clazz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True, help_text='Brief summary shown in listings', max_length=300)),
                ('category', models.CharField(choices=[('news', 'News & Announcements'), ('guide', 'Help & Tutorials'), ('resource', 'Teaching Resources')], default='news', max_length=20)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('featured', models.BooleanField(default=False, help_text='Show on homepage')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-published_at', '-created_at'],
            },
        ),
    ]
