from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("school_admin", "School Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "role"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class TeachingResource(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to="resources/")
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes")
    students = models.ManyToManyField(User, related_name="enrolled_classes", blank=True)
    school = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
