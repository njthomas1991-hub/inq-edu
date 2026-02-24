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

    def __str__(self):
        return self.name


logger = logging.getLogger(__name__)


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
