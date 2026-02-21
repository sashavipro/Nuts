"""about/models.py."""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from home.blocks import (
    AboutBlock,
    StatsBlock,
    EcoBannerBlock,
    HeroBlock,
)
from about.blocks import (
    FounderHistoryBlock,
    WholesaleIntroBlock,
    WholesaleTabsBlock,
)
from contacts.blocks import ContactImportBlock

# pylint: disable=too-few-public-methods


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
                                label=_("Страница галереи"),
                            ),
                        ),
                        (
                            "count",
                            blocks.IntegerBlock(
                                default=3, label=_("Количество элементов")
                            ),
                        ),
                    ],
                    template="about/blocks/gallery_import_wrapper.html",
                    label=_("Импорт галереи"),
                ),
            ),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
        verbose_name=_("Контент страницы"),
    )
    max_count = 1
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [FieldPanel("body")]

    class Meta:
        """Meta options for AboutPage."""

        verbose_name = _("О компании")
        verbose_name_plural = _("О компании")


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
        verbose_name=_("Контент страницы"),
    )
    max_count = 1
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [FieldPanel("body")]

    class Meta:
        """Meta options for WholesalePage."""

        verbose_name = _("Опт и корпоративные клиенты")
        verbose_name_plural = _("Опт и корпоративные клиенты")


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
        verbose_name=_("Контент страницы"),
    )
    max_count = 1
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [FieldPanel("body")]

    class Meta:
        """Meta options for DeliveryPage."""

        verbose_name = _("Оплата и доставка")
        verbose_name_plural = _("Оплата и доставка")
