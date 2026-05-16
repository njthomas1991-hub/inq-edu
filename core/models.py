from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify


# =====================================================
# HELPERS
# =====================================================


def default_avatar_config():
    return {
        "avatar_style": "monster",
        "body_type": "blob",
        "body_color": "#FF6B9D",
        "eye_type": "big_round",
        "mouth_type": "happy",
        "head_decoration": "horns",
        "decoration_color": "#FFB347",
        "pattern": "solid",
        "pattern_color": "#FF1493",
    }


# =====================================================
# SCHOOL MODEL
# =====================================================


class School(models.Model):

    SUBSCRIPTION_CHOICES = (
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    logo = models.ImageField(
        upload_to='school_logos/',
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    subscription_tier = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_CHOICES,
        default='free'
    )

    subscription_active = models.BooleanField(default=True)

    billing_email = models.EmailField(blank=True)

    settings = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


# =====================================================
# USER MODEL
# =====================================================


class User(AbstractUser):

    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('school_admin', 'School Admin'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    display_name = models.CharField(
        max_length=255,
        blank=True
    )

    bio = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"


# =====================================================
# AVATAR MODEL
# =====================================================


class Avatar(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='avatar'
    )

    avatar_config = models.JSONField(
        default=default_avatar_config,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Avatar'
        verbose_name_plural = 'Avatars'

    def __str__(self):
        return f"{self.user.username}'s avatar"

    @property
    def config(self):

        config = default_avatar_config()
        config.update(self.avatar_config or {})

        # Teachers/admins default to human avatars
        if self.user.role in ['teacher', 'school_admin']:
            config['avatar_style'] = 'human'

        return config


# =====================================================
# CLASS MODEL
# =====================================================


class Class(models.Model):

    YEAR_KS_CHOICES = (
        ('EYFS', 'EYFS'),
        ('KS1', 'KS1'),
        ('KS2', 'KS2'),
        ('KS3', 'KS3'),
        ('KS4', 'KS4'),
    )

    SUBJECT_CHOICES = (
        ('english', 'English'),
        ('maths', 'Maths'),
        ('science', 'Science'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('re', 'Religious Education'),
        ('computing', 'Computing'),
    )

    name = models.CharField(max_length=255)

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='classes_taught',
        limit_choices_to={'role': 'teacher'}
    )

    subject = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES
    )

    year_ks = models.CharField(
        max_length=10,
        choices=YEAR_KS_CHOICES
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# =====================================================
# CLASS STUDENT
# =====================================================


class ClassStudent(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled_classes',
        limit_choices_to={'role': 'student'}
    )

    clazz = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='students'
    )

    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'clazz')

    def __str__(self):
        return f"{self.student.username} -> {self.clazz.name}"


# =====================================================
# TEACHING RESOURCES
# =====================================================


class TeachingResource(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    RESOURCE_TYPE_CHOICES = (
        ('lesson_plan', 'Lesson Plan'),
        ('worksheet', 'Worksheet'),
        ('activity', 'Activity'),
        ('presentation', 'Presentation'),
        ('assessment', 'Assessment'),
        ('other', 'Other'),
    )

    KEY_STAGE_CHOICES = (
        ("0", "EYFS"),
        ("1", "KS1"),
        ("2", "KS2"),
        ("3", "KS3"),
        ("4", "KS4"),
    )

    SUBJECT_CHOICES = (
        ("english", "English"),
        ("maths", "Maths"),
        ("science", "Science"),
        ("humanities", "Humanities"),
        ("art", "Art"),
        ("computing", "Computing"),
        ("general", "General"),
    )

    VISIBILITY_CHOICES = (
        ('public', 'Public'),
        ('school', 'School Only'),
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resources'
    )

    content = models.TextField(blank=True)

    excerpt = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='resources/images/',
        blank=True,
        null=True
    )

    file = models.FileField(
        upload_to='resources/files/',
        blank=True,
        null=True
    )

    resource_type = models.CharField(
        max_length=30,
        choices=RESOURCE_TYPE_CHOICES,
        default='other'
    )

    subject = models.CharField(
        max_length=50,
        choices=SUBJECT_CHOICES,
        default='general',
    )

    year_ks = models.CharField(
        max_length=1,
        choices=KEY_STAGE_CHOICES,
        default='2',
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='school'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    featured = models.BooleanField(default=False)

    likes = models.ManyToManyField(
        User,
        related_name='liked_resources',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)


# =====================================================
# RESOURCE COMMENTS
# =====================================================


class ResourceComment(models.Model):

    resource = models.ForeignKey(
        TeachingResource,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resource_comments'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username}"


# =====================================================
# FORUM POSTS
# =====================================================


class ForumPost(models.Model):

    title = models.CharField(max_length=255)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_posts'
    )

    content = models.TextField()

    image = models.ImageField(
        upload_to='forum_posts/',
        blank=True,
        null=True
    )

    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title


# =====================================================
# FORUM REPLIES
# =====================================================


class ForumReply(models.Model):

    post = models.ForeignKey(
        ForumPost,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_replies'
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username}"


# =====================================================
# NEWS ANNOUNCEMENTS
# =====================================================


class NewsAnnouncement(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news_posts'
    )

    content = models.TextField()

    excerpt = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='news/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# =====================================================
# HELP TUTORIALS
# =====================================================


class HelpTutorial(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tutorials'
    )

    content = models.TextField()

    excerpt = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='tutorials/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# =====================================================
# SCHOOL ANALYTICS
# =====================================================


class SchoolAnalyticsProfile(models.Model):

    teacher = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='analytics_profile'
    )

    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analytics_profiles'
    )

    can_access_all_teachers = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.username} analytics"


# =====================================================
# KINDLEWICK GAME PROGRESS
# =====================================================


class KindlewickGameProgress(models.Model):

    GAME_TYPES = (
        ('map', 'Map Exploration'),
        ('castle', 'Wizard Castle'),
        ('potions', 'Prefixes Potions'),
        ('grid', 'Grid Coordinator'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='game_progress'
    )

    game_type = models.CharField(
        max_length=50,
        choices=GAME_TYPES
    )

    current_level = models.IntegerField(default=1)

    score = models.IntegerField(default=0)

    tokens_earned = models.IntegerField(default=0)

    total_playtime = models.IntegerField(default=0)

    completed = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'game_type')

    def __str__(self):
        return f"{self.user.username} - {self.game_type}"


# =====================================================
# KINDLEWICK GAME SESSION
# =====================================================


class KindlewickGameSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='game_sessions'
    )

    game_type = models.CharField(max_length=50)

    level = models.IntegerField(default=1)

    score = models.IntegerField(default=0)

    playtime = models.IntegerField(default=0)

    session_data = models.JSONField(default=dict, blank=True)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} session"








