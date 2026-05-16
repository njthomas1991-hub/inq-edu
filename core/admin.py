from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from django_summernote.admin import SummernoteModelAdmin

from .models import (
    User,
    School,
    Avatar,
    Class,
    ClassStudent,
    TeachingResource,
    ResourceComment,
    ForumPost,
    ForumReply,
    NewsAnnouncement,
    HelpTutorial,
    SchoolAnalyticsProfile,
    KindlewickGameProgress,
    KindlewickGameSession,
)

# =====================================================
# REMOVE GROUP
# =====================================================

admin.site.unregister(Group)


# =====================================================
# HELPERS
# =====================================================

def _is_teacher(user):

    return (
        user.is_authenticated
        and getattr(user, "role", None) == "teacher"
    )


# =====================================================
# USER ADMIN
# =====================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):

    model = User

    llist_display = (
    'username',
    'first_name',
    'last_name',
    'role',
    'school',
    'is_staff',
    'is_active',
)

    list_filter = (
        'role',
        'school',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    ordering = ('username',)

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'password',
                )
            }
        ),

        (
            'Personal Information',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'display_name',
                    'bio',
                )
            }
        ),

        (
            'School Information',
            {
                'fields': (
                    'role',
                    'school',
                )
            }
        ),

        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),

        (
            'Important Dates',
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'role',
                    'school',
                ),
            },
        ),
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if _is_teacher(request.user):
            return qs.filter(role='student')

        return qs.none()

    def has_view_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True

        if _is_teacher(request.user):

            if obj is None:
                return True

            return obj.role == 'student'

        return False

    def has_add_permission(self, request):

        return (
            request.user.is_superuser
            or _is_teacher(request.user)
        )

    def has_change_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True

        if _is_teacher(request.user):

            if obj is None:
                return True

            return obj.role == 'student'

        return False

    def has_delete_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True

        if _is_teacher(request.user):

            if obj is None:
                return True

            return obj.role == 'student'

        return False


# =====================================================
# SCHOOL ADMIN
# =====================================================

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'subscription_tier',
        'subscription_active',
        'created_at',
    )

    search_fields = (
        'name',
        'billing_email',
    )

    list_filter = (
        'subscription_tier',
        'subscription_active',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    readonly_fields = (
        'created_at',
        'updated_at'
    )


# =====================================================
# AVATAR ADMIN
# =====================================================

@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        (
            'User',
            {
                'fields': (
                    'user',
                )
            }
        ),

        (
            'Avatar Configuration',
            {
                'fields': (
                    'avatar_config',
                )
            }
        ),

        (
            'Metadata',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )


# =====================================================
# CLASS STUDENT INLINE
# =====================================================

class ClassStudentInline(admin.TabularInline):

    model = ClassStudent

    extra = 1

    readonly_fields = (
        'date_joined',
    )


# =====================================================
# CLASS ADMIN
# =====================================================

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'teacher',
        'subject',
        'year_ks',
        'created_at',
    )

    list_filter = (
        'subject',
        'year_ks',
    )

    search_fields = (
        'name',
        'teacher__username',
    )

    readonly_fields = (
        'created_at',
    )

    inlines = [ClassStudentInline]

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if _is_teacher(request.user):
            return qs.filter(teacher=request.user)

        return qs.none()


# =====================================================
# CLASS STUDENT ADMIN
# =====================================================

@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'clazz',
        'date_joined',
    )

    list_filter = (
        'date_joined',
    )

    search_fields = (
        'student__username',
        'clazz__name',
    )

    readonly_fields = (
        'date_joined',
    )


# =====================================================
# TEACHING RESOURCE ADMIN
# =====================================================

@admin.register(TeachingResource)
class TeachingResourceAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)

    list_display = (
        'title',
        'author',
        'resource_type',
        'subject',
        'year_ks',
        'visibility',
        'status',
        'featured',
        'created_at',
    )

    list_filter = (
        'resource_type',
        'subject',
        'year_ks',
        'visibility',
        'status',
        'featured',
    )

    search_fields = (
        'title',
        'content',
        'subject',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'published_at',
    )

    filter_horizontal = (
        'likes',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    fieldsets = (
        (
            'Content',
            {
                'fields': (
                    'title',
                    'slug',
                    'excerpt',
                    'content',
                )
            }
        ),

        (
            'Media',
            {
                'fields': (
                    'image',
                    'file',
                )
            }
        ),

        (
            'Classification',
            {
                'fields': (
                    'resource_type',
                    'subject',
                    'year_ks',
                    'visibility',
                )
            }
        ),

        (
            'Publishing',
            {
                'fields': (
                    'status',
                    'featured',
                    'published_at',
                )
            }
        ),

        (
            'Engagement',
            {
                'fields': (
                    'likes',
                )
            }
        ),

        (
            'Metadata',
            {
                'fields': (
                    'author',
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if _is_teacher(request.user):
            return qs

        return qs.none()

    def has_view_permission(self, request, obj=None):

        return (
            request.user.is_superuser
            or _is_teacher(request.user)
        )

    def has_add_permission(self, request):

        return (
            request.user.is_superuser
            or _is_teacher(request.user)
        )

    def has_change_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True

        if _is_teacher(request.user):

            if obj is None:
                return True

            return obj.author == request.user

        return False

    def has_delete_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True

        if _is_teacher(request.user):

            if obj is None:
                return False

            return obj.author == request.user

        return False


# =====================================================
# RESOURCE COMMENT ADMIN
# =====================================================

@admin.register(ResourceComment)
class ResourceCommentAdmin(admin.ModelAdmin):

    list_display = (
        'resource',
        'author',
        'created_at',
    )

    search_fields = (
        'content',
    )

    readonly_fields = (
        'created_at',
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# FORUM REPLY INLINE
# =====================================================

class ForumReplyInline(admin.TabularInline):

    model = ForumReply

    extra = 0

    readonly_fields = (
        'author',
        'created_at',
    )


# =====================================================
# FORUM POST ADMIN
# =====================================================

@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'is_pinned',
        'is_locked',
        'views',
        'created_at',
    )

    list_filter = (
        'is_pinned',
        'is_locked',
    )

    search_fields = (
        'title',
        'content',
    )

    readonly_fields = (
        'views',
        'created_at',
        'updated_at',
    )

    inlines = [ForumReplyInline]

    fieldsets = (
        (
            'Post',
            {
                'fields': (
                    'title',
                    'content',
                    'image',
                )
            }
        ),

        (
            'Moderation',
            {
                'fields': (
                    'is_pinned',
                    'is_locked',
                )
            }
        ),

        (
            'Statistics',
            {
                'fields': (
                    'views',
                )
            }
        ),

        (
            'Metadata',
            {
                'fields': (
                    'author',
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# FORUM REPLY ADMIN
# =====================================================

@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):

    list_display = (
        'post',
        'author',
        'created_at',
    )

    search_fields = (
        'content',
    )

    readonly_fields = (
        'created_at',
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# NEWS ADMIN
# =====================================================

@admin.register(NewsAnnouncement)
class NewsAnnouncementAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)

    list_display = (
        'title',
        'author',
        'status',
        'featured',
        'published_at',
    )

    list_filter = (
        'status',
        'featured',
    )

    search_fields = (
        'title',
        'content',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    fieldsets = (
        (
            'Content',
            {
                'fields': (
                    'title',
                    'slug',
                    'excerpt',
                    'content',
                    'image',
                )
            }
        ),

        (
            'Publishing',
            {
                'fields': (
                    'status',
                    'featured',
                    'published_at',
                )
            }
        ),

        (
            'Metadata',
            {
                'fields': (
                    'author',
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# HELP TUTORIAL ADMIN
# =====================================================

@admin.register(HelpTutorial)
class HelpTutorialAdmin(SummernoteModelAdmin):

    summernote_fields = ('content',)

    list_display = (
        'title',
        'author',
        'status',
        'featured',
        'created_at',
    )

    list_filter = (
        'status',
        'featured',
    )

    search_fields = (
        'title',
        'content',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    fieldsets = (
        (
            'Content',
            {
                'fields': (
                    'title',
                    'slug',
                    'excerpt',
                    'content',
                    'image',
                )
            }
        ),

        (
            'Publishing',
            {
                'fields': (
                    'status',
                    'featured',
                )
            }
        ),

        (
            'Metadata',
            {
                'fields': (
                    'author',
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)


# =====================================================
# SCHOOL ANALYTICS
# =====================================================

@admin.register(SchoolAnalyticsProfile)
class SchoolAnalyticsProfileAdmin(admin.ModelAdmin):

    list_display = (
        'teacher',
        'school',
        'can_access_all_teachers',
        'created_at',
    )

    list_filter = (
        'school',
        'can_access_all_teachers',
    )

    search_fields = (
        'teacher__username',
    )

    readonly_fields = (
        'created_at',
    )


# =====================================================
# GAME PROGRESS ADMIN
# =====================================================

@admin.register(KindlewickGameProgress)
class KindlewickGameProgressAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'game_type',
        'current_level',
        'score',
        'tokens_earned',
        'completed',
        'updated_at',
    )

    list_filter = (
        'game_type',
        'completed',
    )

    search_fields = (
        'user__username',
    )


# =====================================================
# GAME SESSION ADMIN
# =====================================================

@admin.register(KindlewickGameSession)
class KindlewickGameSessionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'game_type',
        'level',
        'score',
        'completed',
        'created_at',
    )

    list_filter = (
        'game_type',
        'completed',
    )

    search_fields = (
        'user__username',
    )