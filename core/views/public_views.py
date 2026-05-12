from django.shortcuts import render


def home_page_view(request):
    return render(request, "core/public/home.html")


def about_page_view(request):
    return render(request, "core/public/about.html")


def pricing_page_view(request):
    return render(request, "core/public/pricing.html")


def contact_page_view(request):
    return render(request, "core/public/contact.html")


def kindlewick_page_view(request):
    return render(request, "core/public/kindlewick.html")


def questopia_page_view(request):
    return render(request, "core/public/questopia.html")


def wonderworld_page_view(request):
    return render(request, "core/public/wonderworld.html")