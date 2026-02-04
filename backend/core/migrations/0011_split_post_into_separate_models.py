# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_post'),
    ]

    operations = [
        # Remove the old Post model
        migrations.DeleteModel(
            name='Post',
        ),
        # Create NewsAnnouncement model
        migrations.CreateModel(
            name='NewsAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True, help_text='Brief summary shown in listings', max_length=300)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('featured', models.BooleanField(default=False, help_text='Show on homepage')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News & Announcement',
                'verbose_name_plural': 'News & Announcements',
                'ordering': ['-published_at', '-created_at'],
            },
        ),
        # Create HelpTutorial model
        migrations.CreateModel(
            name='HelpTutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True, help_text='Brief summary shown in listings', max_length=300)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('featured', models.BooleanField(default=False, help_text='Show on homepage')),
                ('order', models.IntegerField(default=0, help_text='Display order (lower numbers first)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Help & Tutorial',
                'verbose_name_plural': 'Help & Tutorials',
                'ordering': ['order', '-published_at', '-created_at'],
            },
        ),
        # Create TeachingResource model
        migrations.CreateModel(
            name='TeachingResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True, help_text='Brief summary shown in listings', max_length=300)),
                ('resource_type', models.CharField(choices=[('lesson_plan', 'Lesson Plan'), ('activity', 'Activity'), ('worksheet', 'Worksheet'), ('physical_material', 'Physical Material'), ('game_setup', 'Game Setup Guide'), ('other', 'Other')], default='other', max_length=20)),
                ('key_stage', models.IntegerField(blank=True, help_text='Key Stage (1-4)', null=True)),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('featured', models.BooleanField(default=False, help_text='Featured resource')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='teaching_resources', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_resources', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Teaching Resource',
                'verbose_name_plural': 'Teaching Resources',
                'ordering': ['-published_at', '-created_at'],
            },
        ),
        # Create ForumPost model
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_pinned', models.BooleanField(default=False, help_text='Pin to top of forum')),
                ('is_locked', models.BooleanField(default=False, help_text='Prevent new replies')),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='forum_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forum Post',
                'verbose_name_plural': 'Forum Posts',
                'ordering': ['-is_pinned', '-updated_at'],
            },
        ),
        # Create ForumReply model
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, related_name='forum_replies', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core.forumpost')),
            ],
            options={
                'verbose_name': 'Forum Reply',
                'verbose_name_plural': 'Forum Replies',
                'ordering': ['created_at'],
            },
        ),
    ]
