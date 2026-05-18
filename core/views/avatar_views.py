import json
import random

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.forms.avatar_forms import AvatarBuilderForm
from core.models import Avatar, default_avatar_config


def _get_or_create_avatar(user):
    avatar, _ = Avatar.objects.get_or_create(
        user=user,
        defaults={"avatar_config": default_avatar_config()},
    )
    return avatar


def _avatar_payload(avatar):
    return {
        "id": avatar.id,
        "user": avatar.user_id,
        "avatar_config": avatar.config,
        "rendered_layers": {
            "background": avatar.config.get("background"),
            "skin": avatar.config.get("skin"),
            "hair": avatar.config.get("hair"),
            "hair_color": avatar.config.get("hair_color"),
            "eyes": avatar.config.get("eyes"),
            "mouth": avatar.config.get("mouth"),
            "outfit": avatar.config.get("outfit"),
            "accessory": avatar.config.get("accessory"),
            "expression": avatar.config.get("expression"),
        },
    }


@login_required
def get_user_avatar(request):
    avatar = _get_or_create_avatar(request.user)
    return JsonResponse(_avatar_payload(avatar))


@csrf_exempt
@login_required
def save_user_avatar(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        payload = request.POST.dict()

    form = AvatarBuilderForm(payload)
    if not form.is_valid():
        return JsonResponse(
            {"error": "Invalid avatar data", "details": form.errors}, status=400
        )

    avatar = _get_or_create_avatar(request.user)
    avatar.avatar_config = form.to_avatar_config()
    avatar.save()

    return JsonResponse(_avatar_payload(avatar))


@login_required
def randomize_avatar(request):
    avatar = _get_or_create_avatar(request.user)

    avatar.avatar_config = {
        "skin": random.choice([choice[0] for choice in Avatar.SKIN_CHOICES]),
        "hair": random.choice([choice[0] for choice in Avatar.HAIR_CHOICES]),
        "hair_color": random.choice(
            [choice[0] for choice in Avatar.HAIR_COLOR_CHOICES]
        ),
        "eyes": random.choice([choice[0] for choice in Avatar.EYES_CHOICES]),
        "mouth": random.choice([choice[0] for choice in Avatar.MOUTH_CHOICES]),
        "outfit": random.choice([choice[0] for choice in Avatar.OUTFIT_CHOICES]),
        "accessory": random.choice([choice[0] for choice in Avatar.ACCESSORY_CHOICES]),
        "background": random.choice(
            [choice[0] for choice in Avatar.BACKGROUND_CHOICES]
        ),
        "expression": random.choice(
            [choice[0] for choice in Avatar.EXPRESSION_CHOICES]
        ),
    }
    avatar.save()

    return JsonResponse(_avatar_payload(avatar))
