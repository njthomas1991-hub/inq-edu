import logging
import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


# Keep role choices at module scope so model import works reliably during app
# initialization.
class Role(models.TextChoices):
    STUDENT = ("student", "Student")
    TEACHER = ("teacher", "Teacher")
    SCHOOL_ADMIN = ("school_admin", "School Admin")


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True)
    # Make `role` required at the model layer; default to 'student' for existing data.
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Classic Django: username is the login field
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(role__in=[Role.TEACHER, Role.SCHOOL_ADMIN]),
                name="unique_email_teacher_admin",
            ),
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        valid = [c.value for c in Role]
        if not self.role or self.role not in valid:
            raise ValidationError({"role": "Invalid or missing role choice"})

        # Enforce unique email among teachers and school_admins at the model layer.
        if self.email and self.role in (Role.TEACHER, Role.SCHOOL_ADMIN):
            qs = User.objects.filter(
                email__iexact=self.email, role__in=(Role.TEACHER, Role.SCHOOL_ADMIN)
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    {
                        "email": "Email is already in use by another teacher or school admin."
                    }
                )

    def save(self, *args, **kwargs):
        # Avoid running full_clean for partial updates (e.g. update_fields used
        # by Django signals like update_last_login). Only validate on full
        # saves to prevent accidental ValidationError during routine partial
        # updates.
        if not kwargs.get("update_fields"):
            # Call full_clean to enforce `clean()` on save so invalid role
            # values are rejected at the model layer regardless of database support.
            self.full_clean()
        return super().save(*args, **kwargs)


class TeachingResource(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resources"
    )
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to="resources/")
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResourceComment(models.Model):
    resource = models.ForeignKey(
        TeachingResource, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="resource_comments"
    )
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
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="LKS2")
    subject = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes")
    students = models.ManyToManyField(User, related_name="enrolled_classes", blank=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft-delete flag: mark a class as deleted without removing DB record.
    # Use `objects` to return only non-deleted classes by default.
    is_deleted = models.BooleanField(default=False)

    # Default manager returns only non-deleted records. Use `all_objects`
    # to access the full table when needed.
    class ClassQuerySet(models.QuerySet):
        def active(self):
            return self.filter(is_deleted=False)

    objects = ClassQuerySet.as_manager()
    all_objects = models.Manager()

    def __str__(self):
        return self.name


class StudentPassword(models.Model):
    """Persistent store for teacher-visible student plaintext passwords.

    WARNING: storing plaintext passwords is a security risk. This model exists
    only to satisfy the current UX requirement that teachers can retrieve
    student passwords even if transient caches are cleared. Consider replacing
    this with one-time reset links or an encrypted secrets store.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="plaintext_password"
    )
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plaintext password for {self.user.username} (stored)"


logger = logging.getLogger(__name__)


class Progress(models.Model):
    """Lightweight progress record for students.

    This model is intentionally minimal — the app can extend it later to
    include detailed per-activity records, timestamps, or aggregate scores.
    """
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress {self.pk} (updated {self.updated_at})"


class StudentProfile(models.Model):
    """Profile for users with the student role.

    - `student_id` is a required, unique identifier for each student.
    - `user` links to the existing `User` model (auth record).
    - `classroom` links to a primary `Class` record.
    - `progress` is an optional reference to the `Progress` record.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    student_id = models.CharField(max_length=50, unique=True)
    classroom = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="student_profiles"
    )
    progress = models.OneToOneField(
        Progress, on_delete=models.SET_NULL, null=True, blank=True, related_name="student"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student {self.student_id} ({self.user.get_full_name()})"


@receiver(pre_save, sender=User)
def prevent_admin_password_change(sender, instance, **kwargs):
    """Prevent changing the password for the `admin` username unless explicitly allowed.

    To allow a change temporarily, set the environment variable
    `ALLOW_ADMIN_PASSWORD_CHANGE=1` for the process that performs the change.
    """
    if instance.username != "admin":
        return
    # If this is a new user (no PK yet) nothing to compare against.
    if not instance.pk:
        return
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    # Password changed?
    if old.password != instance.password:
        if os.environ.get("ALLOW_ADMIN_PASSWORD_CHANGE") == "1":
            logger.info(
                "Admin password change permitted by ALLOW_ADMIN_PASSWORD_CHANGE env var"
            )
            return
        raise PermissionError(
            "Password for 'admin' is locked. Set ALLOW_ADMIN_PASSWORD_CHANGE=1 to allow change."
        )
