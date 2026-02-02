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
    filter_horizontal = ()


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'year_ks', 'created_at')
    list_filter = ('year_ks',)
    search_fields = ('user__username',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'subject', 'year_ks')
    list_filter = ('subject', 'year_ks')
    search_fields = ('name', 'teacher__username')


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'clazz')
    search_fields = ('student__user__username', 'clazz__name')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'started_at', 'score')
    list_filter = ('started_at',)
    search_fields = ('student__user__username',)


@admin.register(LearningObjective)
class LearningObjectiveAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year_ks', 'difficulty', 'description')
    list_filter = ('subject', 'year_ks', 'difficulty')
    search_fields = ('description',)


@admin.register(ObjectiveAttempt)
class ObjectiveAttemptAdmin(admin.ModelAdmin):
    list_display = ('session', 'objective', 'correct', 'attempts')
    list_filter = ('correct',)
    search_fields = ('session__student__user__username', 'objective__description')


@admin.register(StudentObjectiveMastery)
class StudentObjectiveMasteryAdmin(admin.ModelAdmin):
    list_display = ('student', 'objective', 'mastery_score')
    list_filter = ('mastery_score',)
    search_fields = ('student__user__username', 'objective__description')


@admin.register(GameEvent)
class GameEventAdmin(admin.ModelAdmin):
    list_display = ('student', 'event_type', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('student__user__username',)


admin.site.register(User, UserAdmin)
