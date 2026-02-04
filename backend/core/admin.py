from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Class, ClassStudent, SchoolAnalyticsProfile, Post
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_summernote.admin import SummernoteModelAdmin


# Unregister the Group model from admin
admin.site.unregister(Group)


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'featured', 'published_at', 'created_at')
    list_filter = ('status', 'category', 'featured', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'content', 'excerpt')
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'published_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # New post
            obj.author = request.user
        super().save_model(request, obj, form, change)


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'get_full_name', 'role', 'school', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Account', {'fields': ('role', 'school')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    def save_model(self, request, obj, form, change):
        # When adding a new student, set role='student' and inherit teacher's school
        if not change:
            obj.role = 'student'
            if hasattr(request.user, 'school') and request.user.school:
                obj.school = request.user.school
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Teachers only see students (role='student')
        if not request.user.is_superuser and _is_teacher(request.user):
            qs = qs.filter(role='student')
        return qs
    
    def has_view_permission(self, request, obj=None):
        # Superusers can view all users
        if request.user.is_superuser:
            return True
        # Teachers can view students only
        if _is_teacher(request.user):
            return obj is None or obj.role == 'student'
        return False
    
    def has_add_permission(self, request):
        # Superusers and teachers can add students
        return request.user.is_superuser or _is_teacher(request.user)
    
    def has_change_permission(self, request, obj=None):
        # Superusers can change all users
        if request.user.is_superuser:
            return True
        # Teachers can only change students
        if _is_teacher(request.user):
            return obj is None or obj.role == 'student'
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Superusers can delete all users
        if request.user.is_superuser:
            return True
        # Teachers can only delete students
        if _is_teacher(request.user):
            return obj is None or obj.role == 'student'
        return False


def _is_teacher(user):
    return user.is_authenticated and getattr(user, "role", None) == "teacher"


class ClassStudentInline(admin.TabularInline):
    model = ClassStudent
    extra = 1
    readonly_fields = ('date_joined',)
    fields = ('student', 'date_joined')


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'subject', 'year_ks', 'get_student_count', 'created_at')
    list_filter = ('year_ks', 'subject', 'created_at')
    search_fields = ('name', 'teacher__username', 'subject')
    readonly_fields = ('created_at',)
    inlines = [ClassStudentInline]
    
    def get_student_count(self, obj):
        return obj.students.count()
    get_student_count.short_description = 'Students'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Teachers only see their own classes
        if not request.user.is_superuser and request.user.role == 'teacher':
            qs = qs.filter(teacher=request.user)
        return qs

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if _is_teacher(request.user):
            return obj is None or obj.teacher_id == request.user.id
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser or _is_teacher(request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if _is_teacher(request.user):
            return obj is None or obj.teacher_id == request.user.id
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if _is_teacher(request.user):
            return obj is None or obj.teacher_id == request.user.id
        return False


class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'clazz', 'date_joined')
    list_filter = ('date_joined', 'clazz')
    search_fields = ('student__username', 'clazz__name')
    readonly_fields = ('date_joined',)


@admin.register(SchoolAnalyticsProfile)
class SchoolAnalyticsProfileAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'school', 'can_access_all_teachers', 'created_at')
    list_filter = ('school', 'can_access_all_teachers', 'created_at')
    search_fields = ('teacher__username', 'teacher__first_name', 'teacher__last_name', 'school')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('School Admin Info', {'fields': ('teacher', 'school')}),
        ('Permissions', {'fields': ('can_access_all_teachers',)}),
        ('Metadata', {'fields': ('created_at',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if _is_teacher(request.user):
            profile = getattr(request.user, "analytics_profile", None)
            if profile:
                return qs.filter(school=profile.school)
            return qs.none()
        return qs.none()

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if _is_teacher(request.user):
            profile = getattr(request.user, "analytics_profile", None)
            return obj is not None and profile and obj.school == profile.school
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


admin.site.register(User, UserAdmin)
