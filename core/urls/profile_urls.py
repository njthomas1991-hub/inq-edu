from django.urls import path

from core.views.profile_views import (
    profile_view,
    avatar_builder_view,
)

urlpatterns = [
    path(
        "profile/",
        profile_view,
        name="profile",
    ),
    path(
        "profile/avatar/",
        avatar_builder_view,
        name="profile_avatar",
    ),
    path(
        "settings/avatar/",
        avatar_builder_view,
        name="settings_avatar",
    ),
]
