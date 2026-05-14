from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.forms.profile_forms import ProfileForm


@login_required
def profile_view(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
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
        }
    )


@login_required
def account_settings_view(request):

    return render(
        request,
        "core/profile/account_settings.html"
    )