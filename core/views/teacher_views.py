from django.shortcuts import render


def teacher_dashboard_view(request):
    return render(request, "core/teacher/dashboard.html")


def teacher_analytics_view(request):
    return render(request, "core/teacher/teacher_analytics.html")


def class_analytics_view(request, class_id=None):
    return render(request, "core/teacher/class_analytics.html")


def student_analytics_view(request, class_id=None, student_id=None):
    return render(request, "core/teacher/student_analytics.html")


def add_class_view(request):
    return render(request, "core/teacher/add_class.html")


def class_detail_view(request, class_id):
    return render(request, "core/teacher/class_detail.html")


def remove_student_view(request, class_id, student_id):
    return render(request, "core/teacher/remove_student.html")


def transfer_student_view(request, class_id, student_id):
    return render(request, "core/teacher/transfer_student.html")


def teacher_news_list_view(request):
    return render(request, "core/teacher/teacher_news_list.html")


def teacher_news_detail_view(request, slug):
    return render(request, "core/teacher/teacher_news_detail.html")


def teacher_help_list_view(request):
    return render(request, "core/teacher/teacher_help_list.html")


def teacher_help_detail_view(request, slug):
    return render(request, "core/teacher/teacher_help_detail.html")


def teacher_resources_list_view(request):
    return render(request, "core/teacher/teacher_resources_list.html")


def teacher_resource_detail_view(request, slug):
    return render(request, "core/teacher/teacher_resource_detail.html")


def teacher_resource_edit_view(request, slug):
    return render(request, "core/teacher/teacher_resource_edit.html")


def teacher_resource_delete_view(request, slug):
    return render(request, "core/teacher/teacher_resource_delete.html")


def teacher_resource_comment_delete_view(request, slug, comment_id):
    return render(request, "core/teacher/teacher_resource_comment_delete.html")


def teacher_forum_list_view(request):
    return render(request, "core/teacher/teacher_forum_list.html")


def teacher_forum_detail_view(request, post_id):
    return render(request, "core/teacher/teacher_forum_detail.html")


def teacher_forum_edit_view(request, post_id):
    return render(request, "core/teacher/teacher_forum_edit.html")


def teacher_forum_delete_view(request, post_id):
    return render(request, "core/teacher/teacher_forum_delete.html")


def teacher_forum_reply_edit_view(request, post_id, reply_id):
    return render(request, "core/teacher/teacher_forum_reply_edit.html")


def teacher_forum_reply_delete_view(request, post_id, reply_id):
    return render(request, "core/teacher/teacher_forum_reply_delete.html")