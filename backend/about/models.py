"""about/models.py."""

from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from home.blocks import (
    AboutBlock, StatsBlock, MissionBlock, EcoBannerBlock, LatestNewsBlock,
    ContactsMapBlock
)
from about.blocks import (
    ImageBannerBlock, FounderHistoryBlock, SimpleGalleryBlock, WholesaleIntroBlock,
    TextImageBlock, PaymentDeliveryTabsBlock
)


class AboutPage(Page):
    """Page model for the 'About Us' section."""
    # pylint: disable=duplicate-code
    body = StreamField([
        ('banner', ImageBannerBlock()),
        ('about_section', AboutBlock()),
        ('founder', FounderHistoryBlock()),
        ('stats', StatsBlock()),
        ('gallery', SimpleGalleryBlock()),
        ('mission', MissionBlock()),
        ('eco', EcoBannerBlock()),
        ('news', LatestNewsBlock()),
        ('contacts', ContactsMapBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel('body')]


class WholesalePage(Page):
    """Page model for 'Wholesale and Corporate Clients'."""
    body = StreamField([
        ('intro', WholesaleIntroBlock()),
        ('content', TextImageBlock()),
        ('stats', StatsBlock()),
        ('eco', EcoBannerBlock()),
        ('contacts', ContactsMapBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [FieldPanel('body')]


class DeliveryPage(Page):
    """Page model for 'Payment and Delivery' information."""
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, on_delete=models.SET_NULL, related_name='+'
    )
    body = StreamField([
        ('tabs', PaymentDeliveryTabsBlock()),
        ('stats', StatsBlock()),
        ('mission', MissionBlock()),
        ('contacts', ContactsMapBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('hero_image'), FieldPanel('body')
    ]
