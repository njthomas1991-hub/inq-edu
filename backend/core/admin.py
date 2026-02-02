from django.contrib import admin
from .models import User, Class, ClassStudent
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'get_full_name', 'role', 'school', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Account', {'fields': ('role', 'school')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'school', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'subject', 'year_ks', 'created_at')
    list_filter = ('year_ks', 'subject', 'created_at')
    search_fields = ('name', 'teacher__username', 'subject')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Teachers only see their own classes
        if not request.user.is_superuser and request.user.role == 'teacher':
            qs = qs.filter(teacher=request.user)
        return qs


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_obj', 'date_joined')
    list_filter = ('date_joined', 'class_obj')
    search_fields = ('student__username', 'class_obj__name')
    readonly_fields = ('date_joined',)


admin.site.register(User, UserAdmin)
