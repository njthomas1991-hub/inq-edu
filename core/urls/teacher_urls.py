from django.urls import path

from core.views.teacher_views import (

    # DASHBOARD
    teacher_dashboard_view,

    # CLASSES
    teacher_classes_view,
    create_class_view,
    edit_class_view,
    delete_class_view,
    add_student_to_class_view,

    # RESOURCES
    teacher_resources_list_view,
    teacher_resource_create_view,
    teacher_resource_detail_view,
    teacher_resource_edit_view,
    teacher_resource_delete_view,

    # FORUM
    teacher_forum_list_view,
    teacher_forum_create_view,
    teacher_forum_detail_view,
    teacher_forum_edit_view,
    teacher_forum_delete_view,

    # ANALYTICS
    teacher_analytics_view,
)

urlpatterns = [

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "teacher/",
        teacher_dashboard_view,
        name="teacher_dashboard",
    ),

    # =====================================================
    # CLASSES
    # =====================================================

    path(
        "teacher/classes/",
        teacher_classes_view,
        name="teacher_classes",
    ),

    path(
        "teacher/classes/create/",
        create_class_view,
        name="create_class",
    ),

    path(
        "teacher/classes/<int:pk>/edit/",
        edit_class_view,
        name="edit_class",
    ),

    path(
        "teacher/classes/<int:pk>/delete/",
        delete_class_view,
        name="delete_class",
    ),

    path(
        "teacher/classes/<int:pk>/students/add/",
        add_student_to_class_view,
        name="add_student_to_class",
    ),

    # =====================================================
    # RESOURCES CRUD
    # =====================================================

    path(
        "teacher/resources/",
        teacher_resources_list_view,
        name="teacher_resources_list",
    ),

    path(
        "teacher/resources/create/",
        teacher_resource_create_view,
        name="teacher_resource_create",
    ),

    path(
        "teacher/resources/<int:pk>/",
        teacher_resource_detail_view,
        name="teacher_resource_detail",
    ),

    path(
        "teacher/resources/<int:pk>/edit/",
        teacher_resource_edit_view,
        name="teacher_resource_edit",
    ),

    path(
        "teacher/resources/<int:pk>/delete/",
        teacher_resource_delete_view,
        name="teacher_resource_delete",
    ),

    # =====================================================
    # FORUM CRUD
    # =====================================================

    path(
        "teacher/forum/",
        teacher_forum_list_view,
        name="teacher_forum_list",
    ),

    path(
        "teacher/forum/create/",
        teacher_forum_create_view,
        name="teacher_forum_create",
    ),

    path(
        "teacher/forum/<int:pk>/",
        teacher_forum_detail_view,
        name="teacher_forum_detail",
    ),

    path(
        "teacher/forum/<int:pk>/edit/",
        teacher_forum_edit_view,
        name="teacher_forum_edit",
    ),

    path(
        "teacher/forum/<int:pk>/delete/",
        teacher_forum_delete_view,
        name="teacher_forum_delete",
    ),

    # =====================================================
    # ANALYTICS
    # =====================================================

    path(
        "teacher/analytics/",
        teacher_analytics_view,
        name="teacher_analytics",
    ),

]