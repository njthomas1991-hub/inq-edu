from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

EXEMPT_PATH_PREFIXES = (
    "/static/",
    settings.MEDIA_URL,
    settings.STATIC_URL,
    "/admin/",
    "/login/",
    "/logout/",
    "/register/",
    "/accounts/",
    "/wonderworld",
    "/kindlewick",
    "/",
)

# A simple mapping of path prefixes to allowed role values.
# Adjust or extend as needed for your app's routes.
PROTECTED_PATHS = [
    ("/dashboard/", None),  # any authenticated user allowed (views still vary by role)
    ("/teacher/", ("teacher",)),
    ("/school-admin/", ("school_admin",)),
    ("/classes/", ("teacher", "school_admin")),
    ("/class/", ("teacher", "school_admin")),
    ("/resources/", ("teacher",)),
]


class RoleRequiredMiddleware:
    """Middleware to enforce simple role-based access on path prefixes.

    Behavior:
    - Paths starting with any prefix in EXEMPT_PATH_PREFIXES are skipped.
    - For protected prefixes in PROTECTED_PATHS:
        - If allowed_roles is None => require authentication only.
        - Else require request.user.role to be one of allowed_roles.
    - Unauthorised requests are redirected to `LOGIN_URL` if anonymous,
      or return 403 Forbidden if authenticated but lacks role.

    Customize `PROTECTED_PATHS` and `EXEMPT_PATH_PREFIXES` for your app.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Quick exemptions
        for prefix in EXEMPT_PATH_PREFIXES:
            if prefix and path.startswith(prefix):
                return self.get_response(request)

        # Check protected paths
        for prefix, allowed_roles in PROTECTED_PATHS:
            if path.startswith(prefix):
                # Need authentication
                if not request.user.is_authenticated:
                    return redirect(settings.LOGIN_URL + f"?next={request.path}")

                # If allowed_roles is None, any authenticated user may access
                if allowed_roles is None:
                    return self.get_response(request)

                # Role enforcement
                user_role = getattr(request.user, "role", None)
                if user_role in allowed_roles:
                    return self.get_response(request)

                # Authenticated but unauthorized
                try:
                    messages.error(
                        request, "You do not have permission to access that page."
                    )
                except Exception:
                    pass
                return HttpResponseForbidden("Forbidden")

        return self.get_response(request)
