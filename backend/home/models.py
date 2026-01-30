"""home/models.py."""

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from .blocks import (
    HeroBlock, ProductSectionBlock, AboutBlock, StatsBlock,
    MissionBlock, BenefitsBlock, EcoBannerBlock, LatestNewsBlock, ContactsMapBlock
)


class HomePage(Page):
    """The main home page model containing the primary content stream."""
    # pylint: disable=duplicate-code
    body = StreamField([
        ('hero', HeroBlock()),
        ('products', ProductSectionBlock()),
        ('about', AboutBlock()),
        ('stats', StatsBlock()),
        ('mission', MissionBlock()),
        ('benefits', BenefitsBlock()),
        ('eco', EcoBannerBlock()),
        ('news', LatestNewsBlock()),
        ('contacts', ContactsMapBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel('body')]
