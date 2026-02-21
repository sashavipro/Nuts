"""gallery/models.py."""

import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from home.blocks import HeroBlock
from gallery.blocks import GallerySectionBlock
from contacts.blocks import ContactImportBlock

logger = logging.getLogger(__name__)


class GalleryPage(Page):  # pylint: disable=too-many-ancestors
    """
    The main gallery page model.
    Displays images in a grid with pagination and HTMX support.
    """

    body = StreamField(
        [
            ("hero", HeroBlock(group=_("Основное"))),
            ("gallery_section", GallerySectionBlock()),
            ("contacts_section", ContactImportBlock(group=_("Основное"))),
        ],
        use_json_field=True,
        verbose_name=_("Контент страницы"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options for GalleryPage."""

        verbose_name = _("Галерея")
        verbose_name_plural = _("Галереи")

    def get_main_gallery_section(self):
        """
        Retrieves the first gallery section block from the body.
        """
        # pylint: disable=not-an-iterable
        for block in self.body:
            if block.block_type == "gallery_section":
                return block.value
        return None

    def get_context(self, request, *args, **kwargs):
        """
        Adds paginated gallery items to the template context.
        """
        context = super().get_context(request, *args, **kwargs)
        gallery_data = self.get_main_gallery_section()

        if gallery_data:
            all_items = gallery_data.get("items")
            per_page = gallery_data.get("items_per_page", 6)

            paginator = Paginator(all_items, per_page)
            page_number = request.GET.get("page")

            try:
                gallery_items = paginator.page(page_number)
            except PageNotAnInteger:
                gallery_items = paginator.page(1)
            except EmptyPage:
                gallery_items = []

            context["gallery_items"] = gallery_items
            # pylint: disable=no-member
            logger.debug(
                "GalleryPage %s: Returning %s items for page %s",
                self.id,
                len(gallery_items),
                page_number,
            )

        return context

    def serve(self, request, *args, **kwargs):
        """
        Handles the request. Intercepts HTMX requests to return only the gallery items partial.
        """
        if request.headers.get("HX-Request"):
            # pylint: disable=no-member
            logger.info(
                "HTMX Request detected on GalleryPage %s. Page: %s",
                self.id,
                request.GET.get("page"),
            )

            context = self.get_context(request, *args, **kwargs)
            return TemplateResponse(
                request, "gallery/includes/gallery_items.html", context
            )

        return super().serve(request, *args, **kwargs)
