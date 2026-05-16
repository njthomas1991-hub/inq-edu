from django.urls import path

from core.views.profile_views import (
    account_settings_view,
    avatar_builder_view,
    profile_view,
)


urlpatterns = [
    path("profile/", profile_view, name="profile"),
    path("profile/avatar/", avatar_builder_view, name="profile_avatar"),
    path("settings/avatar/", avatar_builder_view, name="settings_avatar"),
    path("account-settings/", account_settings_view, name="account_settings"),
]