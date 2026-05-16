from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Avatar


@login_required
def profile_view(request):

    avatar, created = Avatar.objects.get_or_create(
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

from core.models import Avatar


@login_required
def avatar_builder_view(request):

    avatar, created = Avatar.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        avatar.avatar_type = request.POST.get(
            "avatar_type",
            avatar.avatar_type,
        )

        avatar.body_color = request.POST.get(
            "body_color",
            avatar.body_color,
        )

        avatar.eye_type = request.POST.get(
            "eye_type",
            avatar.eye_type,
        )

        avatar.mouth_type = request.POST.get(
            "mouth_type",
            avatar.mouth_type,
        )

        avatar.save()

        return redirect("profile")

    context = {
        "avatar": avatar,
    }

    return render(
        request,
        "profiles/avatar_builder.html",
        context,
    )