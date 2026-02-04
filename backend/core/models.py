from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.text import slugify

# User Model - Teachers and Students
class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.CharField(max_length=255, null=True, blank=True)
    plain_password = models.CharField(max_length=100, null=True, blank=True, help_text="Plain text password for display purposes (students only)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Teacher Sign-up'
        verbose_name_plural = 'Teacher Sign-ups'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


# Class Model - Created by teachers
class Class(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'}, related_name='classes_taught')
    subject = models.CharField(max_length=100)
    year_ks = models.IntegerField()  # Key Stage (1-4)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.name} - {self.subject} (KS{self.year_ks})"


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


# Post Model - News, guides, and educational resources
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CATEGORY_CHOICES = (
        ('news', 'News & Announcements'),
        ('guide', 'Help & Tutorials'),
        ('resource', 'Teaching Resources'),
    )
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Brief summary shown in listings")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='news')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Post'
        verbose_name_plural = "Posts"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title