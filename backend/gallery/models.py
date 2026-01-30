"""gallery/models.py."""

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable
from home.blocks import ContactsMapBlock


class GalleryImage(Orderable):
    """Represents a single image or video item within the gallery page."""
    page = ParentalKey(
        'GalleryPage',
        related_name='gallery_items', on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE, related_name='+'
    )
    video_url = models.URLField(blank=True)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.TextField(blank=True)

    SIZE_CHOICES = [('full', 'Full'), ('half', 'Half'), ('third', 'Third')]
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='third')

    panels = [
        FieldPanel('image'), FieldPanel('size'),
        MultiFieldPanel(
            [FieldPanel('video_url'), FieldPanel('title'), FieldPanel('subtitle')]
        ),
    ]


class GalleryPage(Page):  # pylint: disable=too-many-ancestors
    """Page model designed to display a grid of gallery images and videos."""
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, on_delete=models.SET_NULL, related_name='+'
    )
    hero_subtitle = models.CharField(max_length=255, default="Кадры активности")
    footer_blocks = StreamField(
        [('contacts', ContactsMapBlock())],
        use_json_field=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('hero_image'), FieldPanel('hero_subtitle'),
        InlinePanel('gallery_items', label="Галерея"),
        FieldPanel('footer_blocks')
    ]
