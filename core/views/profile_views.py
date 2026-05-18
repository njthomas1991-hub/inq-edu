from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.shortcuts import (
    render,
    redirect,
)

from django.utils import timezone

from core.models import Avatar

from core.forms.profile_forms import (
    ProfileForm,
)

# =====================================================
# AVATAR OPTIONS
# =====================================================

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
        "sad",
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


# =====================================================
# PROFILE VIEW
# =====================================================


@login_required
def profile_view(request):

    avatar, _ = Avatar.objects.get_or_create(user=request.user)

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )

        if form.is_valid():

            user = form.save(commit=False)

            user.last_active = timezone.now()

            user.save()

            messages.success(
                request,
                "Profile updated successfully.",
            )

            return redirect("/profile/?updated=avatar")

        else:

            messages.error(
                request,
                "Please correct the errors below.",
            )

    else:

        form = ProfileForm(instance=request.user)

    context = {
        "form": form,
        "avatar": avatar,
        "page_title": "My Profile",
    }

    return render(
        request,
        "core/profile/profile.html",
        context,
    )


# =====================================================
# AVATAR BUILDER
# =====================================================


@login_required
def avatar_builder_view(request):

    avatar, _ = Avatar.objects.get_or_create(user=request.user)

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

        request.user.last_active = timezone.now()

        request.user.save()

        messages.success(
            request,
            "Avatar updated successfully.",
        )

        return redirect("profile")

    context = {
        "avatar": avatar,
        "config": config,
        "avatar_options": AVATAR_OPTIONS,
        "page_title": "Avatar Builder",
    }

    return render(
        request,
        "core/profile/avatar_builder.html",
        context,
    )
