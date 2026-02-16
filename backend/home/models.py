"""home/models.py."""

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from contacts.blocks import ContactImportBlock
from .blocks import (
    HeroBlock,
    AboutBlock,
    StatsBlock,
    BenefitsBlock,
    EcoBannerBlock,
    LatestNewsBlock,
)


class HomePage(Page):  # pylint: disable=too-many-ancestors
    """
    The main home page model containing the primary content stream.
    """

    # pylint: disable=duplicate-code
    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("about", AboutBlock()),
            ("stats", StatsBlock()),
            ("benefits", BenefitsBlock()),
            ("eco", EcoBannerBlock()),
            ("news", LatestNewsBlock()),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("body")]

    max_count = 1
    parent_page_types = []
