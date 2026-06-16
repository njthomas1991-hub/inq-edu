from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Avatar, KindlewickGameProgress, KindlewickGameSession, User
from core.serializers import (
    AvatarSerializer,
    KindlewickGameProgressAdminSerializer,
    KindlewickGameProgressSerializer,
    KindlewickGameSessionAdminSerializer,
    KindlewickGameSessionSerializer,
    UserSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user_api(request):
    user_data = dict(UserSerializer(request.user).data)

    monster_avatar = Avatar.objects.filter(user=request.user).first()

    user_data["monster_avatar"] = (
        AvatarSerializer(monster_avatar).data if monster_avatar else None
    )

    return Response(user_data)


def custom_404_view(request, exception=None):

    if request.headers.get("accept", "").startswith("application/json"):

        return JsonResponse({"error": "Not found"}, status=404)

    return JsonResponse({"error": "Page not found"}, status=404)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def kindlewick_progress_list(request):
    if request.method == "GET":
        queryset = KindlewickGameProgress.objects.filter(user=request.user).order_by(
            "-updated_at"
        )
        return Response(KindlewickGameProgressSerializer(queryset, many=True).data)

    serializer = KindlewickGameProgressSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def kindlewick_sessions(request):
    if request.method == "GET":
        queryset = KindlewickGameSession.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        return Response(KindlewickGameSessionSerializer(queryset, many=True).data)

    serializer = KindlewickGameSessionSerializer(data=request.data)

    if serializer.is_valid():
        session = serializer.save(user=request.user)
        return Response(KindlewickGameSessionSerializer(session).data, status=201)

    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def kindlewick_session_detail(request, session_id):
    session = get_object_or_404(KindlewickGameSession, pk=session_id, user=request.user)

    if request.method == "GET":
        return Response(KindlewickGameSessionSerializer(session).data)

    if request.method == "DELETE":
        session.delete()
        return Response(status=204)

    serializer = KindlewickGameSessionSerializer(session, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kindlewick_teacher_progress(request):
    queryset = KindlewickGameProgress.objects.all().order_by("-updated_at")

    if request.user.role == "teacher" and request.user.school_id:
        queryset = queryset.filter(user__school=request.user.school)
    elif request.user.role == "school_admin" and request.user.school_id:
        queryset = queryset.filter(user__school=request.user.school)

    student_id = request.GET.get("student_id")
    teacher_id = request.GET.get("teacher_id")

    if student_id:
        queryset = queryset.filter(user_id=student_id)
    elif teacher_id:
        queryset = queryset.filter(user__school_id=teacher_id)

    return Response(KindlewickGameProgressAdminSerializer(queryset, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kindlewick_teacher_sessions(request):
    queryset = KindlewickGameSession.objects.all().order_by("-created_at")

    if request.user.role == "teacher" and request.user.school_id:
        queryset = queryset.filter(user__school=request.user.school)
    elif request.user.role == "school_admin" and request.user.school_id:
        queryset = queryset.filter(user__school=request.user.school)

    student_id = request.GET.get("student_id")
    teacher_id = request.GET.get("teacher_id")

    if student_id:
        queryset = queryset.filter(user_id=student_id)
    elif teacher_id:
        queryset = queryset.filter(user__school_id=teacher_id)

    return Response(KindlewickGameSessionAdminSerializer(queryset, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kindlewick_school_admin_progress(request):
    return kindlewick_teacher_progress(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kindlewick_school_admin_sessions(request):
    return kindlewick_teacher_sessions(request)
