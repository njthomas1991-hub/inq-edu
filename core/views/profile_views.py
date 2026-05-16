from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.forms.avatar_forms import AvatarBuilderForm
from core.forms.profile_forms import ProfileForm
from core.models import Avatar, default_avatar_config


@login_required
def profile_view(request):

    avatar, _ = Avatar.objects.get_or_create(
        user=request.user,
        defaults={"avatar_config": default_avatar_config()},
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(instance=request.user)

    return render(
        request,
        "core/profile/profile.html",
        {
            "form": form,
            "avatar": avatar,
        }
    )


@login_required
def account_settings_view(request):

    return render(
        request,
        "core/profile/account_settings.html"
    )


@login_required
def avatar_builder_view(request):

    avatar, _ = Avatar.objects.get_or_create(
        user=request.user,
        defaults={"avatar_config": default_avatar_config()},
    )

    if request.method == "POST":

        form = AvatarBuilderForm(request.POST)

        if form.is_valid():
            avatar.avatar_config = form.to_avatar_config()
            avatar.save()

            messages.success(
                request,
                "Avatar updated successfully."
            )

            return redirect(request.path)

    else:

        form = AvatarBuilderForm(initial=avatar.config)

    return render(
        request,
        "core/profile/avatar_builder.html",
        {
            "form": form,
            "avatar": avatar,
            "avatar_config": avatar.config,
        }
    )