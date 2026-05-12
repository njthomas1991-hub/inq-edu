from django.http import JsonResponse
from django.utils import timezone

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    KindlewickGameProgress,
    KindlewickGameSession,
    User,
)

from core.serializers import (
    UserSerializer,
    AvatarSerializer,
    KindlewickGameProgressSerializer,
    KindlewickGameSessionSerializer,
    KindlewickGameProgressAdminSerializer,
    KindlewickGameSessionAdminSerializer,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_api(request):

    avatar = getattr(request.user, 'avatar', None)

    user_data = dict(
        UserSerializer(request.user).data
    )

    user_data['avatar'] = (
        AvatarSerializer(avatar).data
        if avatar else None
    )

    return Response(user_data)


def custom_404_view(request, exception=None):

    if request.headers.get('accept', '').startswith('application/json'):

        return JsonResponse(
            {'error': 'Not found'},
            status=404
        )

    return JsonResponse(
        {'error': 'Page not found'},
        status=404
    )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def kindlewick_progress_list(request):

    return Response(
        {"message": "kindlewick_progress_list working"}
    )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def kindlewick_sessions(request):

    return Response(
        {"message": "kindlewick_sessions working"}
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def kindlewick_session_detail(request, session_id):

    return Response(
        {
            "message": "kindlewick_session_detail working",
            "session_id": session_id
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_teacher_progress(request):

    return Response(
        {"message": "kindlewick_teacher_progress working"}
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_teacher_sessions(request):

    return Response(
        {"message": "kindlewick_teacher_sessions working"}
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_school_admin_progress(request):

    return Response(
        {"message": "kindlewick_school_admin_progress working"}
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kindlewick_school_admin_sessions(request):

    return Response(
        {"message": "kindlewick_school_admin_sessions working"}
    )