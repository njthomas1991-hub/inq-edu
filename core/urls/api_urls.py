from django.urls import path

from core.views.api_views import (
    hello,
    get_user_avatar,
    save_user_avatar,
    randomize_avatar,
    current_user_api,
    kindlewick_progress_list,
    kindlewick_sessions,
    kindlewick_session_detail,
    kindlewick_teacher_progress,
    kindlewick_teacher_sessions,
    kindlewick_school_admin_progress,
    kindlewick_school_admin_sessions,
    create_student_account_view,
)

from core.views.avatar_views import (
    get_user_avatar,
    save_user_avatar,
    randomize_avatar,
)

urlpatterns = [

    path(
        "api/hello/",
        hello,
        name="api_hello"
    ),

    path(
        "api/create-student/",
        create_student_account_view,
        name="create_student"
    ),

    path(
        "api/avatar/",
        get_user_avatar,
        name="get_avatar"
    ),

    path(
        "api/avatar/save/",
        save_user_avatar,
        name="save_avatar"
    ),

    path(
        "api/avatar/randomize/",
        randomize_avatar,
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