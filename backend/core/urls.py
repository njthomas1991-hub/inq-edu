from django.urls import path
from .views import home_page_view, hello

urlpatterns = [
    path("", home_page_view),
    path("api/hello/", hello),
]
