import random

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
        ("free", "Free"),
        ("pro", "Pro"),
        ("enterprise", "Enterprise"),
    )

    name = models.CharField(max_length=255, unique=True)

    slug = models.SlugField(unique=True, blank=True)

    logo = models.ImageField(upload_to="school_logos/", blank=True, null=True)

    description = models.TextField(blank=True)

    subscription_tier = models.CharField(
        max_length=20, choices=SUBSCRIPTION_CHOICES, default="free"
    )

    subscription_active = models.BooleanField(default=True)

    billing_email = models.EmailField(blank=True)

    settings = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["name"]

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
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("school_admin", "School Admin"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    school = models.ForeignKey(
        School, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )

    display_name = models.CharField(max_length=255, blank=True)

    bio = models.TextField(blank=True, null=True)

    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )

    plain_password = models.CharField(max_length=255, blank=True, null=True)

    total_xp = models.IntegerField(default=0)

    level = models.IntegerField(default=1)

    streak = models.IntegerField(default=0)

    tokens = models.IntegerField(default=0)

    achievements = models.JSONField(default=list, blank=True)

    last_active = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["username"]

    def __str__(self):

        return f"{self.username} ({self.role})"

    @property
    def full_name(self):

        full = (f"{self.first_name} " f"{self.last_name}").strip()

        return full if full else self.username

    @property
    def initials(self):

        first = self.first_name[:1] if self.first_name else ""
        last = self.last_name[:1] if self.last_name else ""

        return f"{first}{last}".upper()


# =====================================================
# AVATAR MODEL
# =====================================================


class Avatar(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="avatar")

    avatar_config = models.JSONField(default=default_avatar_config, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.user.username}'s avatar"


# =====================================================
# CLASS MODEL
# =====================================================


class Class(models.Model):

    YEAR_KS_CHOICES = (
        ("EYFS", "EYFS"),
        ("KS1", "KS1"),
        ("KS2", "KS2"),
        ("KS3", "KS3"),
        ("KS4", "KS4"),
    )

    SUBJECT_CHOICES = (
        ("english", "English"),
        ("maths", "Maths"),
        ("science", "Science"),
        ("history", "History"),
        ("geography", "Geography"),
        ("re", "Religious Education"),
        ("computing", "Computing"),
    )

    name = models.CharField(max_length=255)

    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="classes_taught"
    )

    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)

    year_ks = models.CharField(max_length=10, choices=YEAR_KS_CHOICES)

    description = models.TextField(blank=True)

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_archived = models.BooleanField(default=False)

    class Meta:

        ordering = ["name"]

    def __str__(self):

        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# =====================================================
# CLASS STUDENT
# =====================================================


class ClassStudent(models.Model):

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enrolled_classes"
    )

    clazz = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="students")

    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ("student", "clazz")

    def __str__(self):

        return f"{self.student.username} -> {self.clazz.name}"


# =====================================================
# TEACHING RESOURCES
# =====================================================


class TeachingResource(models.Model):

    RESOURCE_TYPE_CHOICES = (
        ("lesson_plan", "Lesson Plan"),
        ("worksheet", "Worksheet"),
        ("activity", "Activity"),
        ("presentation", "Presentation"),
        ("assessment", "Assessment"),
        ("other", "Other"),
    )

    YEAR_KS_CHOICES = (
        ("0", "EYFS"),
        ("1", "KS1"),
        ("2", "KS2"),
        ("3", "KS3"),
        ("4", "KS4"),
    )

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("school", "School Only"),
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resources")

    description = models.TextField(blank=True)

    uploaded_file = models.FileField(
        upload_to="resources/uploads/", blank=True, null=True
    )

    image = models.ImageField(upload_to="resources/images/", blank=True, null=True)

    resource_type = models.CharField(
        max_length=100, choices=RESOURCE_TYPE_CHOICES, default="other"
    )

    subject = models.CharField(max_length=100, blank=True)

    year_ks = models.CharField(max_length=50, choices=YEAR_KS_CHOICES, blank=True)

    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="school"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    featured = models.BooleanField(default=False)

    allow_comments = models.BooleanField(default=True)

    likes_count = models.IntegerField(default=0)

    is_flagged = models.BooleanField(default=False)

    moderation_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:

        ordering = ["-created_at"]

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(self.title) or "resource"
            slug = base_slug
            counter = 1

            while (
                TeachingResource.objects.filter(slug=slug).exclude(pk=self.pk).exists()
            ):

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)


# =====================================================
# RESOURCE COMMENTS
# =====================================================


class ResourceComment(models.Model):

    resource = models.ForeignKey(
        TeachingResource, on_delete=models.CASCADE, related_name="comments"
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"Comment by {self.author.username}"


# =====================================================
# RESOURCE LIKES
# =====================================================


class ResourceLike(models.Model):

    resource = models.ForeignKey(
        TeachingResource, on_delete=models.CASCADE, related_name="resource_likes"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ("resource", "user")


# =====================================================
# FORUM POSTS
# =====================================================


class ForumPost(models.Model):

    VISIBILITY_CHOICES = (
        ("public", "Public"),
        ("school", "School Only"),
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="forum_posts"
    )

    image = models.ImageField(upload_to="forum/images/", blank=True, null=True)

    uploaded_file = models.FileField(upload_to="forum/uploads/", blank=True, null=True)

    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="public"
    )

    allow_replies = models.BooleanField(default=True)

    likes_count = models.IntegerField(default=0)

    is_pinned = models.BooleanField(default=False)

    is_locked = models.BooleanField(default=False)

    is_flagged = models.BooleanField(default=False)

    moderation_notes = models.TextField(blank=True)

    views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-is_pinned", "-updated_at"]

    def __str__(self):

        return self.title


# =====================================================
# FORUM REPLIES
# =====================================================


class ForumReply(models.Model):

    post = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="replies"
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"Reply by {self.author.username}"


# =====================================================
# FORUM POST LIKES
# =====================================================


class ForumPostLike(models.Model):

    post = models.ForeignKey(
        ForumPost, on_delete=models.CASCADE, related_name="post_likes"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ("post", "user")


# =====================================================
# NEWS ANNOUNCEMENTS
# =====================================================


class NewsAnnouncement(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    image = models.ImageField(upload_to="news/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.title


# =====================================================
# HELP TUTORIALS
# =====================================================


class HelpTutorial(models.Model):

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()

    image = models.ImageField(upload_to="tutorials/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.title


# =====================================================
# GAME PROGRESS
# =====================================================


class KindlewickGameProgress(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="game_progress"
    )

    game_type = models.CharField(max_length=100)

    current_level = models.IntegerField(default=1)

    score = models.IntegerField(default=0)

    tokens_earned = models.IntegerField(default=0)

    total_playtime = models.IntegerField(default=0)

    completed = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)


# =====================================================
# GAME SESSION
# =====================================================


class KindlewickGameSession(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="game_sessions"
    )

    game_type = models.CharField(max_length=100)

    level = models.IntegerField(default=1)

    score = models.IntegerField(default=0)

    playtime = models.IntegerField(default=0)

    session_data = models.JSONField(default=dict, blank=True)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


# =====================================================
# STUDENT ANALYTICS
# =====================================================


class StudentAnalytics(models.Model):

    student = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_analytics"
    )

    total_logins = models.IntegerField(default=0)

    lessons_completed = models.IntegerField(default=0)

    resources_viewed = models.IntegerField(default=0)

    forum_posts = models.IntegerField(default=0)

    forum_replies = models.IntegerField(default=0)

    games_played = models.IntegerField(default=0)

    total_score = models.IntegerField(default=0)

    attendance_percentage = models.FloatField(default=100)

    engagement_score = models.FloatField(default=0)

    last_seen = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Student Analytics"

    def __str__(self):

        return f"{self.student.username} analytics"


# =====================================================
# CLASS ANALYTICS
# =====================================================


class ClassAnalytics(models.Model):

    clazz = models.OneToOneField(
        Class, on_delete=models.CASCADE, related_name="analytics"
    )

    total_students = models.IntegerField(default=0)

    active_students = models.IntegerField(default=0)

    average_xp = models.IntegerField(default=0)

    total_resources = models.IntegerField(default=0)

    total_discussions = models.IntegerField(default=0)

    average_engagement = models.FloatField(default=0)

    leaderboard_enabled = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Class Analytics"

    def __str__(self):

        return f"{self.clazz.name} analytics"


# =====================================================
# RESOURCE ANALYTICS
# =====================================================


class ResourceAnalytics(models.Model):

    resource = models.OneToOneField(
        TeachingResource, on_delete=models.CASCADE, related_name="analytics"
    )

    views = models.IntegerField(default=0)

    downloads = models.IntegerField(default=0)

    shares = models.IntegerField(default=0)

    comments = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    bookmarks = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Resource Analytics"

    def __str__(self):

        return f"{self.resource.title} analytics"


# =====================================================
# FORUM ANALYTICS
# =====================================================


class ForumAnalytics(models.Model):

    post = models.OneToOneField(
        ForumPost, on_delete=models.CASCADE, related_name="analytics"
    )

    views = models.IntegerField(default=0)

    replies = models.IntegerField(default=0)

    likes = models.IntegerField(default=0)

    reports = models.IntegerField(default=0)

    moderation_actions = models.IntegerField(default=0)

    engagement_score = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "Forum Analytics"

    def __str__(self):

        return f"{self.post.title} analytics"


# =====================================================
# SCHOOL ANALYTICS PROFILE
# =====================================================


class SchoolAnalyticsProfile(models.Model):

    school = models.OneToOneField(
        School, on_delete=models.CASCADE, related_name="analytics"
    )

    total_teachers = models.IntegerField(default=0)

    total_students = models.IntegerField(default=0)

    total_classes = models.IntegerField(default=0)

    total_resources = models.IntegerField(default=0)

    total_forum_posts = models.IntegerField(default=0)

    total_game_sessions = models.IntegerField(default=0)

    safeguarding_flags = models.IntegerField(default=0)

    average_engagement = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name_plural = "School Analytics Profiles"

    def __str__(self):

        return f"{self.school.name} analytics"
