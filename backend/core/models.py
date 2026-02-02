from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# User Model - Teachers and Students
class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'class_obj')
        verbose_name_plural = "Class Students"

    def __str__(self):
        return f"{self.student.username} in {self.class_obj.name}"