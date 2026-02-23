from django.contrib import admin
from .models import User, TeachingResource, Class

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "role", "school")
    search_fields = ("email", "first_name", "last_name", "role", "school")

@admin.register(TeachingResource)
class TeachingResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "uploaded_at")
    search_fields = ("title", "teacher__email")

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "school")
    search_fields = ("name", "teacher__email", "school")
