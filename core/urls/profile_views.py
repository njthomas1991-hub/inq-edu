from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def profile_view(request):

    if request.method == 'POST':

        bio = request.POST.get('bio', '').strip()

        request.user.bio = bio
        request.user.save()

        messages.success(
            request,
            'Profile updated successfully!'
        )

        return redirect('profile')

    return render(
        request,
        'core/profile/profile.html'
    )


@login_required
def account_settings_view(request):

    return render(
        request,
        'core/profile/account_settings.html'
    )