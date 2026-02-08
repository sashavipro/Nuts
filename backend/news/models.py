"""news/models.py."""

from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from home.blocks import ContactsMapBlock


class NewsPage(Page):
    """Page model for a single news article or post."""

    date = models.DateField("Дата")
    intro = models.TextField("Краткое описание")
    feed_image = models.ForeignKey(
        "wagtailimages.Image", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    is_video_post = models.BooleanField(default=False)

    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("video_embed", blocks.URLBlock()),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("feed_image"),
        FieldPanel("is_video_post"),
        FieldPanel("intro"),
        FieldPanel("body"),
    ]

    parent_page_types = ["NewsIndexPage"]
    subpage_types = []


class NewsIndexPage(Page):
    """Page model that displays a list of news articles."""

    subpage_types = ["NewsPage"]

    footer_blocks = StreamField(
        [("contacts", ContactsMapBlock())], use_json_field=True, blank=True
    )

    content_panels = Page.content_panels + [FieldPanel("footer_blocks")]
