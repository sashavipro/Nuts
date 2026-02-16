"""about/models.py."""

from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from home.blocks import (
    AboutBlock,
    StatsBlock,
    EcoBannerBlock,
    LatestNewsBlock,
    HeroBlock,
)
from about.blocks import (
    FounderHistoryBlock,
    WholesaleIntroBlock,
    WholesaleTabsBlock,
)
from contacts.blocks import ContactImportBlock


class AboutPage(Page):  # pylint: disable=too-many-ancestors
    """Page model for the About section."""

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("about_section", AboutBlock()),
            ("founder", FounderHistoryBlock()),
            ("stats", StatsBlock()),
            (
                "gallery_import",
                blocks.StructBlock(
                    [
                        (
                            "gallery_page",
                            blocks.PageChooserBlock(
                                target_model="gallery.GalleryPage",
                                label="Страница галереи",
                            ),
                        ),
                        (
                            "count",
                            blocks.IntegerBlock(
                                default=3, label="Количество элементов"
                            ),
                        ),
                    ],
                    template="about/blocks/gallery_import_wrapper.html",
                    label="Вставка Галереи",
                ),
            ),
            ("eco", EcoBannerBlock()),
            ("news", LatestNewsBlock()),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
    )
    max_count = 1
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [FieldPanel("body")]


class WholesalePage(Page):  # pylint: disable=too-many-ancestors
    """Page model for 'Wholesale and Corporate Clients'."""

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("intro", WholesaleIntroBlock()),
            ("tabs_section", WholesaleTabsBlock()),
            ("stats", StatsBlock()),
            ("eco", EcoBannerBlock()),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
    )
    max_count = 1
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [FieldPanel("body")]


class DeliveryPage(Page):  # pylint: disable=too-many-ancestors
    """Page model for 'Payment and Delivery' information."""

    body = StreamField(
        [
            ("hero", HeroBlock()),
            ("intro", WholesaleIntroBlock()),
            ("tabs_section", WholesaleTabsBlock()),
            ("stats", StatsBlock()),
            ("eco", EcoBannerBlock()),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
    )
    max_count = 1
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [FieldPanel("body")]
