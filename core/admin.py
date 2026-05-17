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
    ResourceLike,
    ForumPost,
    ForumReply,
    ForumPostLike,
    NewsAnnouncement,
    HelpTutorial,
    SchoolAnalyticsProfile,
    StudentAnalytics,
    ClassAnalytics,
    ResourceAnalytics,
    ForumAnalytics,
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

    list_display = (
        'username',
        'first_name',
        'last_name',
        'role',
        'school',
        'level',
        'tokens',
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
                    'profile_image',
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
            'Gamification',
            {
                'fields': (
                    'total_xp',
                    'level',
                    'streak',
                    'tokens',
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
                    'created_at',
                    'updated_at',
                )
            }
        ),
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


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

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }


# =====================================================
# AVATAR ADMIN
# =====================================================

@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'updated_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


# =====================================================
# CLASS INLINE
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

    search_fields = (
        'student__username',
        'clazz__name',
    )


# =====================================================
# RESOURCE ADMIN
# =====================================================

@admin.register(TeachingResource)
class TeachingResourceAdmin(SummernoteModelAdmin):

    summernote_fields = (
        'description',
    )

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
        'visibility',
        'status',
        'featured',
    )

    search_fields = (
        'title',
        'description',
        'subject',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'published_at',
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
                    'description',
                )
            }
        ),

        (
            'Media',
            {
                'fields': (
                    'image',
                    'uploaded_file',
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
                    'allow_comments',
                    'published_at',
                )
            }
        ),

        (
            'Moderation',
            {
                'fields': (
                    'is_flagged',
                    'moderation_notes',
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


# =====================================================
# RESOURCE LIKE ADMIN
# =====================================================

@admin.register(ResourceLike)
class ResourceLikeAdmin(admin.ModelAdmin):

    list_display = (
        'resource',
        'user',
        'created_at',
    )


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
class ForumPostAdmin(SummernoteModelAdmin):

    summernote_fields = (
        'description',
    )

    list_display = (
        'title',
        'author',
        'visibility',
        'is_pinned',
        'is_locked',
        'views',
        'created_at',
    )

    list_filter = (
        'visibility',
        'is_pinned',
        'is_locked',
    )

    search_fields = (
        'title',
        'description',
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
                    'description',
                    'image',
                    'uploaded_file',
                )
            }
        ),

        (
            'Settings',
            {
                'fields': (
                    'visibility',
                    'allow_replies',
                )
            }
        ),

        (
            'Moderation',
            {
                'fields': (
                    'is_pinned',
                    'is_locked',
                    'is_flagged',
                    'moderation_notes',
                )
            }
        ),

        (
            'Statistics',
            {
                'fields': (
                    'views',
                    'likes_count',
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


# =====================================================
# FORUM POST LIKE ADMIN
# =====================================================

@admin.register(ForumPostLike)
class ForumPostLikeAdmin(admin.ModelAdmin):

    list_display = (
        'post',
        'user',
        'created_at',
    )


# =====================================================
# NEWS ADMIN
# =====================================================

@admin.register(NewsAnnouncement)
class NewsAnnouncementAdmin(SummernoteModelAdmin):

    summernote_fields = (
        'content',
    )

    list_display = (
        'title',
        'author',
        'created_at',
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


# =====================================================
# HELP ADMIN
# =====================================================

@admin.register(HelpTutorial)
class HelpTutorialAdmin(SummernoteModelAdmin):

    summernote_fields = (
        'content',
    )

    list_display = (
        'title',
        'author',
        'created_at',
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


# =====================================================
# STUDENT ANALYTICS
# =====================================================

@admin.register(StudentAnalytics)
class StudentAnalyticsAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'games_played',
        'total_score',
        'engagement_score',
        'updated_at',
    )


# =====================================================
# CLASS ANALYTICS
# =====================================================

@admin.register(ClassAnalytics)
class ClassAnalyticsAdmin(admin.ModelAdmin):

    list_display = (
        'clazz',
        'total_students',
        'average_xp',
        'average_engagement',
        'updated_at',
    )


# =====================================================
# RESOURCE ANALYTICS
# =====================================================

@admin.register(ResourceAnalytics)
class ResourceAnalyticsAdmin(admin.ModelAdmin):

    list_display = (
        'resource',
        'views',
        'downloads',
        'likes',
        'updated_at',
    )


# =====================================================
# FORUM ANALYTICS
# =====================================================

@admin.register(ForumAnalytics)
class ForumAnalyticsAdmin(admin.ModelAdmin):

    list_display = (
        'post',
        'views',
        'replies',
        'likes',
        'updated_at',
    )


# =====================================================
# SCHOOL ANALYTICS
# =====================================================

@admin.register(SchoolAnalyticsProfile)
class SchoolAnalyticsProfileAdmin(admin.ModelAdmin):

    list_display = (
        'school',
        'total_teachers',
        'total_students',
        'average_engagement',
        'updated_at',
    )


# =====================================================
# GAME PROGRESS
# =====================================================

@admin.register(KindlewickGameProgress)
class KindlewickGameProgressAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'game_type',
        'current_level',
        'score',
        'completed',
    )


# =====================================================
# GAME SESSION
# =====================================================

@admin.register(KindlewickGameSession)
class KindlewickGameSessionAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'game_type',
        'level',
        'score',
        'created_at',
    )