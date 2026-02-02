from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# -----------------------------
# 1. Users & Roles
# -----------------------------
class School(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    # first_name, last_name, username, password are inherited
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

# -----------------------------
# 2. Classes & Enrollment
# -----------------------------
class Class(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    year_ks = models.IntegerField()
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.subject})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    year_ks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()

class ClassStudent(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('student', 'clazz')

# -----------------------------
# 3. Sessions (analytics)
# -----------------------------
class Session(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    clazz = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    engagement_time_seconds = models.FloatField(default=0)
    session_duration_seconds = models.FloatField(default=0)
    score = models.FloatField(default=0)

# -----------------------------
# 4. Learning Objectives
# -----------------------------
class LearningObjective(models.Model):
    subject = models.CharField(max_length=100)
    year_ks = models.IntegerField()
    difficulty = models.IntegerField(default=3)
    description = models.TextField()

    def __str__(self):
        return f"{self.subject} - KS{self.year_ks} - {self.description[:50]}"

class ObjectiveAttempt(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attempts')
    objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    attempts = models.IntegerField(default=1)
    time_spent_seconds = models.FloatField(default=0)

# -----------------------------
# 5. Mastery Tracking
# -----------------------------
class StudentObjectiveMastery(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    mastery_score = models.FloatField(default=0)  # 0.0 to 1.0
    confidence = models.FloatField(default=0)     # optional: predictive confidence
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'objective')

# -----------------------------
# 6. Gamification events
# -----------------------------
class GameEvent(models.Model):
    EVENT_TYPES = (
        ('badge', 'Badge'),
        ('level_up', 'Level Up'),
        ('streak', 'Streak'),
        ('retry', 'Retry'),
    )
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_value = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)