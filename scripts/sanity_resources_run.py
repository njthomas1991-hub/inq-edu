import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inclusive_quest_education.settings")
import django

django.setup()

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.test import Client

from quest_app.models import TeachingResource

User = get_user_model()

u, created = User.objects.get_or_create(
    username="test_teacher",
    defaults={
        "email": "test_teacher@example.com",
        "first_name": "Test",
        "role": "teacher",
    },
)
if created:
    u.set_password("testpass")
    u.save()

for i in range(1, 15):
    title = f"Auto Resource {i}"
    if not TeachingResource.objects.filter(title=title, teacher=u).exists():
        f = ContentFile(b"hello world", name=f"resource{i}.txt")
        res = TeachingResource(
            teacher=u, title=title, description="Auto-generated for smoke test"
        )
        res.document.save(f"resource{i}.txt", f, save=True)

client = Client()
logged = client.login(username="test_teacher", password="testpass")
print("login", logged)
resp = client.get("/teacher-resources/?page=1&partial=1")
print("status", resp.status_code)
print("len", len(resp.content))
print("has_load_more", b"Load more" in resp.content)
print("has_page_link", b"resource-page-link" in resp.content)
