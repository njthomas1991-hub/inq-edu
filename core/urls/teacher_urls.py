from django.urls import path

from core.views.teacher_views import (
    teacher_dashboard_view,
    teacher_analytics_view,
    add_class_view,
    class_detail_view,
    class_analytics_view,
    student_analytics_view,
    remove_student_view,
    transfer_student_view,
    teacher_news_list_view,
    teacher_news_detail_view,
    teacher_help_list_view,
    teacher_help_detail_view,
    teacher_resources_list_view,
    teacher_resource_detail_view,
    teacher_resource_edit_view,
    teacher_resource_delete_view,
    teacher_resource_comment_delete_view,
    teacher_forum_list_view,
    teacher_forum_detail_view,
    teacher_forum_edit_view,
    teacher_forum_delete_view,
    teacher_forum_reply_edit_view,
    teacher_forum_reply_delete_view,
    profile_view,
    account_settings_view,
)

urlpatterns = [

    path("teacher/", teacher_dashboard_view, name="teacher_dashboard"),

    path(
        "teacher/analytics/",
        teacher_analytics_view,
        name="teacher_analytics"
    ),

    path(
        "teacher/class/add/",
        add_class_view,
        name="add_class"
    ),

    path(
        "teacher/class/<int:class_id>/",
        class_detail_view,
        name="class_detail"
    ),

    path(
        "teacher/class/<int:class_id>/analytics/",
        class_analytics_view,
        name="class_analytics"
    ),

    path(
        "teacher/class/<int:class_id>/student/<int:student_id>/analytics/",
        student_analytics_view,
        name="student_analytics"
    ),

    path(
        "teacher/class/<int:class_id>/remove/<int:student_id>/",
        remove_student_view,
        name="remove_student"
    ),

    path(
        "teacher/class/<int:class_id>/transfer/<int:student_id>/",
        transfer_student_view,
        name="transfer_student"
    ),

    path(
        "teacher/news/",
        teacher_news_list_view,
        name="teacher_news"
    ),

    path(
        "teacher/news/<slug:slug>/",
        teacher_news_detail_view,
        name="teacher_news_detail"
    ),

    path(
        "teacher/help/",
        teacher_help_list_view,
        name="teacher_help"
    ),

    path(
        "teacher/help/<slug:slug>/",
        teacher_help_detail_view,
        name="teacher_help_detail"
    ),

    path(
        "teacher/resources/",
        teacher_resources_list_view,
        name="teacher_resources"
    ),

    path(
        "teacher/resources/<slug:slug>/",
        teacher_resource_detail_view,
        name="teacher_resource_detail"
    ),

    path(
        "teacher/resources/<slug:slug>/edit/",
        teacher_resource_edit_view,
        name="teacher_resource_edit"
    ),

    path(
        "teacher/resources/<slug:slug>/delete/",
        teacher_resource_delete_view,
        name="teacher_resource_delete"
    ),

    path(
        "teacher/resources/<slug:slug>/comment/<int:comment_id>/delete/",
        teacher_resource_comment_delete_view,
        name="teacher_resource_comment_delete"
    ),

    path(
        "teacher/forum/",
        teacher_forum_list_view,
        name="teacher_forum"
    ),

    path(
        "teacher/forum/<int:post_id>/",
        teacher_forum_detail_view,
        name="teacher_forum_detail"
    ),

    path(
        "teacher/forum/<int:post_id>/edit/",
        teacher_forum_edit_view,
        name="teacher_forum_edit"
    ),

    path(
        "teacher/forum/<int:post_id>/delete/",
        teacher_forum_delete_view,
        name="teacher_forum_delete"
    ),

    path(
        "teacher/forum/<int:post_id>/reply/<int:reply_id>/edit/",
        teacher_forum_reply_edit_view,
        name="teacher_forum_reply_edit"
    ),

    path(
        "teacher/forum/<int:post_id>/reply/<int:reply_id>/delete/",
        teacher_forum_reply_delete_view,
        name="teacher_forum_reply_delete"
    ),

    path(
        "profile/",
        profile_view,
        name="profile"
    ),

    path(
        "account-settings/",
        account_settings_view,
        name="account_settings"
    ),
]