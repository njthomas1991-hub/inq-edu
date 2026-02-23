from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    email = models.EmailField(blank=True, null=True)
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("school_admin", "School Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    # Classic Django: username is the login field
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class TeachingResource(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to="resources/")
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ResourceComment(models.Model):
    resource = models.ForeignKey(TeachingResource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.resource.title}"

class Class(models.Model):
    name = models.CharField(max_length=100)
    LEVEL_CHOICES = [
        ("EYFS", "EYFS"),
        ("KS1", "KS1"),
        ("LKS2", "LKS2"),
        ("UKS2", "UKS2"),
        ("KS3", "KS3"),
        ("KS4", "KS4"),
        ("SEND", "SEND"),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='LKS2')
    subject = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes")
    students = models.ManyToManyField(User, related_name="enrolled_classes", blank=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
