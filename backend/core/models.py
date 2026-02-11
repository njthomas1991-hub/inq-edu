from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify
# Cloudinary removed - not used in new avatar system

# User Model - Teachers and Students
class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('school_admin', 'School Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    school = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    plain_password = models.CharField(max_length=100, null=True, blank=True, help_text="Plain text password for display purposes (students only)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Teacher Sign-up'
        verbose_name_plural = 'Teacher Sign-ups'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


# Class Model - Created by teachers
class Class(models.Model):
    KEY_STAGE_CHOICES = (
        (0, "EYFS"),
        (1, "KS1"),
        (2, "KS2"),
        (3, "KS3"),
        (4, "KS4"),
    )
    SUBJECT_CHOICES = (
        ("english", "English"),
        ("maths", "Maths"),
        ("english_maths", "English and Maths"),
    )

    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='classes_taught')
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    year_ks = models.IntegerField(choices=KEY_STAGE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.key_stage_label})"

    @property
    def key_stage_label(self):
        if self.year_ks == 0:
            return "EYFS"
        return f"KS{self.year_ks}"

    @property
    def subject_label(self):
        return self.get_subject_display()


# ClassStudent Model - Students enrolled in a class
class ClassStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='enrolled_classes')
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'clazz')
        verbose_name_plural = "Class Students"

    def __str__(self):
        return f"{self.student.username} in {self.clazz.name}"


# SchoolAnalyticsProfile Model - School admins who can access multiple teachers' data
class SchoolAnalyticsProfile(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='analytics_profile')
    school = models.CharField(max_length=255)
    can_access_all_teachers = models.BooleanField(default=True, help_text="Access all teachers' data in the same school")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "School Analytics Profiles"

    def __str__(self):
        return f"{self.teacher.get_full_name() or self.teacher.username} (Admin) - {self.school}"


# NewsAnnouncement Model - Admin only
class NewsAnnouncement(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary shown in listings")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'News & Announcement'
        verbose_name_plural = "News & Announcements"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# HelpTutorial Model - Admin only
class HelpTutorial(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='help_posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary shown in listings")
    image = models.ImageField(upload_to='help_tutorials/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['order', '-published_at', '-created_at']
        verbose_name = 'Help & Tutorial'
        verbose_name_plural = "Help & Tutorials"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


# TeachingResource Model - Shared by teachers
class TeachingResource(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    RESOURCE_TYPE_CHOICES = (
        ('lesson_plan', 'Lesson Plan'),
        ('activity', 'Activity'),
        ('worksheet', 'Worksheet'),
        ('physical_material', 'Physical Material'),
        ('game_setup', 'Game Setup Guide'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='teaching_resources')
    content = models.TextField(blank=True)
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary shown in listings")
    image = models.ImageField(upload_to='teaching_resources/images/', blank=True, null=True)
    file = models.FileField(upload_to='teaching_resources/', blank=True, null=True, help_text="Upload PDF, Word, Excel files")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES, default='other')
    key_stage = models.IntegerField(null=True, blank=True, help_text="Key Stage (1-4)")
    subject = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Featured resource")
    likes = models.ManyToManyField(User, related_name='liked_resources', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Teaching Resource'
        verbose_name_plural = "Teaching Resources"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while TeachingResource.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.likes.count()


# ForumPost Model - Community discussions
class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='forum_posts')
    content = models.TextField()
    image = models.ImageField(upload_to='forum_posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False, help_text="Pin to top of forum")
    is_locked = models.BooleanField(default=False, help_text="Prevent new replies")
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-is_pinned', '-updated_at']
        verbose_name = 'Forum Post'
        verbose_name_plural = "Forum Posts"
    
    def __str__(self):
        return self.title
    
    @property
    def replies_count(self):
        return self.replies.count()


# ForumReply Model - Replies to forum posts
class ForumReply(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='forum_replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Forum Reply'
        verbose_name_plural = "Forum Replies"
    
    def __str__(self):
        return f"Reply by {self.author.username} on {self.post.title}"


# ResourceComment Model - Comments on teaching resources
class ResourceComment(models.Model):
    resource = models.ForeignKey(TeachingResource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='resource_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Resource Comment'
        verbose_name_plural = "Resource Comments"
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.resource.title}"


# Avatar Model - PixiJS sprite-based monster avatars
class Avatar(models.Model):
    """ClassDojo-style monster avatar"""
    
    BODY_TYPES = (
        ('blob', 'Blob'),
        ('round', 'Round'),
        ('tall', 'Tall'),
        ('wide', 'Wide'),
        ('pear', 'Pear'),
        ('bean', 'Bean'),
    )
    
    EYE_TYPES = (
        ('big_round', 'Big Round'),
        ('small_dots', 'Small Dots'),
        ('one_eye', 'One Eye'),
        ('sleepy', 'Sleepy'),
        ('googly', 'Googly'),
        ('angry', 'Angry'),
    )
    
    MOUTH_TYPES = (
        ('happy', 'Happy'),
        ('toothy', 'Toothy'),
        ('small', 'Small'),
        ('big_smile', 'Big Smile'),
        ('oh', 'Oh'),
        ('silly', 'Silly'),
    )
    
    DECORATION_TYPES = (
        ('none', 'None'),
        ('horns', 'Horns'),
        ('antennae', 'Antennae'),
        ('spikes', 'Spikes'),
        ('ears', 'Ears'),
        ('mohawk', 'Mohawk'),
    )
    
    PATTERN_TYPES = (
        ('solid', 'Solid'),
        ('spots', 'Spots'),
        ('stripes', 'Stripes'),
        ('gradient', 'Gradient'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    
    # Body
    body_type = models.CharField(max_length=20, choices=BODY_TYPES, default='blob')
    body_color = models.CharField(max_length=7, default='#FF6B9D', help_text='Hex color')
    
    # Facial features
    eye_type = models.CharField(max_length=20, choices=EYE_TYPES, default='big_round')
    mouth_type = models.CharField(max_length=20, choices=MOUTH_TYPES, default='happy')
    
    # Head decorations (horns, antennae, etc)
    head_decoration = models.CharField(max_length=20, choices=DECORATION_TYPES, default='horns')
    decoration_color = models.CharField(max_length=7, default='#FFB347', help_text='Hex color')
    
    # Pattern/texture
    pattern = models.CharField(max_length=20, choices=PATTERN_TYPES, default='solid')
    pattern_color = models.CharField(max_length=7, default='#FF1493', help_text='Hex color for spots/stripes')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Avatar'
        verbose_name_plural = 'User Avatars'
    
    def __str__(self):
        return f"Avatar for {self.user.username}"
    
    def to_dict(self):
        """Convert avatar to dictionary for frontend"""
        return {
            'id': self.id,
            'userId': self.user.id,
            'bodyType': self.body_type,
            'bodyColor': self.body_color,
            'eyeType': self.eye_type,
            'mouthType': self.mouth_type,
            'headDecoration': self.head_decoration,
            'decorationColor': self.decoration_color,
            'pattern': self.pattern,
            'patternColor': self.pattern_color,
        }