from django.urls import path

from core.views.legal_views import (
    terms_of_use,
    subscription_details,
    privacy_policy,
    accessibility_statement,
)

urlpatterns = [
    path('terms-of-use/', terms_of_use, name='terms_of_use'),
    path('subscription-details/', subscription_details, name='subscription_details'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('accessibility-statement/', accessibility_statement, name='accessibility_statement'),
]