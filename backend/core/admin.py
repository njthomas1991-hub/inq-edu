from django.contrib import admin
from .models import (
    User, School, StudentProfile, Class, ClassStudent, Session,
    LearningObjective, ObjectiveAttempt, StudentObjectiveMastery, GameEvent
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role', 'school')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'school', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()  # Remove groups and user_permissions


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'year_ks')
    list_filter = ('year_ks',)
    search_fields = ('user__username',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'subject', 'year_ks')
    list_filter = ('subject', 'year_ks')
    search_fields = ('name', 'teacher__username')


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('student__username', 'class_obj__name')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_time', 'score')
    list_filter = ('start_time',)
    search_fields = ('student__username',)


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year_ks', 'difficulty', 'description')
    list_filter = ('subject', 'year_ks', 'difficulty')
    search_fields = ('description',)


@admin.register(ObjectiveAttempt)
class ObjectiveAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'objective', 'success', 'timestamp')
    list_filter = ('success', 'timestamp')
    search_fields = ('student__username', 'objective__description')


@admin.register(StudentObjectiveMastery)
class StudentObjectiveMasteryAdmin(admin.ModelAdmin):
    list_display = ('student', 'objective', 'mastery_level')
    list_filter = ('mastery_level',)
    search_fields = ('student__username', 'objective__description')


@admin.register(GameEvent)
class GameEventAdmin(admin.ModelAdmin):
    list_display = ('student', 'event_type', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('student__username',)


admin.site.register(User, UserAdmin)
