"""users/models/profile.py."""

from django.db import models
from django.shortcuts import render
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from contacts.blocks import ContactImportBlock


class ProfilePage(RoutablePageMixin, Page):  # pylint: disable=too-many-ancestors
    """User profile page managing dashboard, orders, and addresses."""

    promo_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    promo_text = models.CharField(
        max_length=255, blank=True, default="Орех Причерноморья"
    )

    footer_blocks = StreamField(
        [
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("promo_image"),
        FieldPanel("promo_text"),
        FieldPanel("footer_blocks"),
    ]

    @route(r"^$")
    def dashboard(self, request):
        """Render the main dashboard view."""
        return render(request, "users/profile_dashboard.html", {"page": self})

    @route(r"^orders/$")
    def orders(self, request):
        """Render the order history view."""
        return render(request, "users/profile_orders.html", {"page": self})

    @route(r"^address/$")
    def address(self, request):
        """Render the address settings view."""
        return render(request, "users/profile_address.html", {"page": self})
