from django.urls import path

from core.views.api_views import (
    current_user_api,
    kindlewick_progress_list,
    kindlewick_sessions,
    kindlewick_session_detail,
    kindlewick_teacher_progress,
    kindlewick_teacher_sessions,
    kindlewick_school_admin_progress,
    kindlewick_school_admin_sessions,
    )

from core.views import api_views
from core.views import avatar_views


def _resolve_create_student_account_view(request, *args, **kwargs):
    """Resolve create student account view at runtime to avoid static attribute issues."""
    view = getattr(api_views, "create_student_account_view", None) or getattr(api_views, "create_student_account", None)
    if view is None:
        raise AttributeError("No create student account view found on core.views.api_views")
    return view(request, *args, **kwargs)


def _resolve_avatar_view(request, *args, **kwargs):
    """Resolve avatar view at runtime to avoid static attribute issues."""
    view = getattr(avatar_views, "get_user_avatar", None) or getattr(avatar_views, "save_user_avatar", None)
    if view is None:
        raise AttributeError("No avatar view found on core.views.avatar_views")
    return view(request, *args, **kwargs)


def _resolve_save_avatar_view(request, *args, **kwargs):
    """Resolve save avatar view at runtime to avoid static attribute issues."""
    view = getattr(avatar_views, "save_user_avatar", None)
    if view is None:
        raise AttributeError("save_user_avatar not found on core.views.avatar_views")
    return view(request, *args, **kwargs)


def _resolve_randomize_avatar_view(request, *args, **kwargs):
    """Resolve randomize avatar view at runtime to avoid static attribute issues."""
    view = getattr(avatar_views, "randomize_avatar", None)
    if view is None:
        raise AttributeError("randomize_avatar not found on core.views.avatar_views")
    return view(request, *args, **kwargs)

urlpatterns = [

    path(
        "api/create-student/",
        _resolve_create_student_account_view,
        name="create_student"
    ),

    path(
        "api/avatar/",
        _resolve_avatar_view,
        name="get_avatar"
    ),

    path(
        "api/avatar/save/",
        _resolve_save_avatar_view,
        name="save_avatar"
    ),

    path(
        "api/avatar/randomize/",
        _resolve_randomize_avatar_view,
        name="randomize_avatar"
    ),

    path(
        "api/user/current/",
        current_user_api,
        name="api_current_user"
    ),

    path(
        "api/kindlewick/progress/",
        kindlewick_progress_list,
        name="api_kindlewick_progress"
    ),

    path(
        "api/kindlewick/sessions/",
        kindlewick_sessions,
        name="api_kindlewick_sessions"
    ),

    path(
        "api/kindlewick/sessions/<int:session_id>/",
        kindlewick_session_detail,
        name="api_kindlewick_session_detail"
    ),

    path(
        "api/kindlewick/teacher/progress/",
        kindlewick_teacher_progress,
        name="api_kindlewick_teacher_progress"
    ),

    path(
        "api/kindlewick/teacher/sessions/",
        kindlewick_teacher_sessions,
        name="api_kindlewick_teacher_sessions"
    ),

    path(
        "api/kindlewick/school-admin/progress/",
        kindlewick_school_admin_progress,
        name="api_kindlewick_school_admin_progress"
    ),

    path(
        "api/kindlewick/school-admin/sessions/",
        kindlewick_school_admin_sessions,
        name="api_kindlewick_school_admin_sessions"
    ),
]