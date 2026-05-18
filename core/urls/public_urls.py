from django.urls import path

from core.views.public_views import (
    hello,
    home_page_view,
    about_page_view,
    kindlewick_page_view,
    wonderworld_page_view,
    questopia_page_view,
    pricing_page_view,
    teacher_hub_view,
    contact_page_view,
)

urlpatterns = [
    path("", home_page_view, name="home"),
    path("about/", about_page_view, name="about"),
    path("kindlewick/", kindlewick_page_view, name="kindlewick"),
    path("wonderworld/", wonderworld_page_view, name="wonderworld"),
    path("questopia/", questopia_page_view, name="questopia"),
    path("pricing/", pricing_page_view, name="pricing"),
    path("teacher-hub/", teacher_hub_view, name="teacher_hub"),
    path("contact/", contact_page_view, name="contact"),
    path("api/hello/", hello, name="api_hello"),
]
