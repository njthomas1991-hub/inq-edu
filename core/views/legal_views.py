from django.shortcuts import render


def terms_of_use(request):

    return render(request, "core/public/terms_of_use.html")


def subscription_details(request):

    return render(request, "core/public/subscription_detials.html")


def privacy_policy(request):

    return render(request, "core/public/privacy_policy.html")


def accessibility_statement(request):

    return render(request, "core/public/accessibility_statement.html")
