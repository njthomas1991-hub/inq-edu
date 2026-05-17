from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.models import Avatar


AVATAR_OPTIONS = {
    "avatar_style": [
        "monster",
        "human",
        "robot",
    ],
    "body_type": [
        "blob",
        "round",
        "square",
    ],
    "eye_type": [
        "big_round",
        "sleepy",
        "star",
        "laser",
    ],
    "mouth_type": [
        "happy",
        "smile",
        "grin",
        "surprised",
    ],
    "head_decoration": [
        "horns",
        "hat",
        "crown",
        "none",
    ],
}


@login_required
def profile_view(request):

    avatar, _ = Avatar.objects.get_or_create(
        user=request.user
    )

    context = {
        "avatar": avatar,
    }

    return render(
        request,
        "core/profile/profile.html",
        context,
    )


@login_required
def avatar_builder_view(request):

    avatar, _ = Avatar.objects.get_or_create(
        user=request.user
    )

    config = avatar.avatar_config or {}

    if request.method == "POST":

        config["avatar_style"] = request.POST.get(
            "avatar_style",
            "monster",
        )

        config["body_type"] = request.POST.get(
            "body_type",
            "blob",
        )

        config["body_color"] = request.POST.get(
            "body_color",
            "#FF6B9D",
        )

        config["eye_type"] = request.POST.get(
            "eye_type",
            "big_round",
        )

        config["mouth_type"] = request.POST.get(
            "mouth_type",
            "happy",
        )

        config["head_decoration"] = request.POST.get(
            "head_decoration",
            "horns",
        )

        config["decoration_color"] = request.POST.get(
            "decoration_color",
            "#FFB347",
        )

        avatar.avatar_config = config
        avatar.save()

        return redirect("profile")

    context = {
        "avatar": avatar,
        "config": config,
        "avatar_options": AVATAR_OPTIONS,
    }

    return render(
        request,
        "core/profile/avatar_builder.html",
        context,
    )