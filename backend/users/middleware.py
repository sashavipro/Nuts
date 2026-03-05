"""users/middleware.py."""

import logging

from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class RestrictStaffToAdminMiddleware:
    """Redirects staff and superusers to the admin panel (Unfold or Wagtail).

    Triggers if they try to access the public storefront.
    """

    def __init__(self, get_response):
        """Initialize the middleware with the given get_response callable."""
        self.get_response = get_response

    def __call__(self, request):
        """Process the request and restrict staff access to public views."""
        user = request.user
        path = request.path_info

        if user.is_authenticated and (user.is_staff or user.is_superuser):
            try:
                django_admin_prefix = reverse("admin:index")
            except Exception:  # pylint: disable=broad-exception-caught # noqa: BLE001
                django_admin_prefix = "/django-admin/"

            allowed_prefixes = (
                django_admin_prefix,
                "/admin/",
                "/static/",
                "/media/",
                "/__debug__/",
            )

            if not path.startswith(allowed_prefixes):
                logger.info(
                    "Staff user '%s' attempted to access public path '%s'. "
                    "Redirecting to admin.",
                    user.username,
                    path,
                )
                return redirect(django_admin_prefix)

        return self.get_response(request)
