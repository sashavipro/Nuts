"""gallery/models.py."""

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from home.blocks import ContactsMapBlock, HeroBlock
from gallery.blocks import GallerySectionBlock


class GalleryPage(Page):
    """
    The main gallery page.
    """

    body = StreamField(
        [
            ("hero", HeroBlock(group="Основные")),
            ("gallery_section", GallerySectionBlock()),
            ("contacts", ContactsMapBlock(group="Основные")),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_main_gallery_section(self):
        """
        Finds the first 'gallery_section' block in the body and returns its value.
        Used for importing into other pages.
        """
        for block in self.body:
            if block.block_type == "gallery_section":
                return block.value
        return None
