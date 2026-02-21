"""home/models.py."""

from django.utils.translation import gettext_lazy as _
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
            ("hero", HeroBlock(label=_("Главный экран (Hero)"))),
            ("about", AboutBlock(label=_("Блок 'О производителе'"))),
            ("stats", StatsBlock(label=_("Блок статистики"))),
            ("benefits", BenefitsBlock(label=_("Блок преимуществ"))),
            ("eco", EcoBannerBlock(label=_("Эко баннер"))),
            ("news", LatestNewsBlock(label=_("Последние новости"))),
            ("contacts_section", ContactImportBlock(label=_("Блок контактов"))),
        ],
        use_json_field=True,
        verbose_name=_("Контент страницы"),
    )

    content_panels = Page.content_panels + [FieldPanel("body")]

    max_count = 1
    parent_page_types = []

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options for HomePage."""

        verbose_name = _("Главная страница")
        verbose_name_plural = _("Главные страницы")
