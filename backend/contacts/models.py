"""contacts/models.py"""

import logging
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from home.blocks import HeroBlock
from .blocks import DetailedContactsBlock

logger = logging.getLogger(__name__)


class ContactPage(Page):
    """
    Page model for the 'Contact Us' page.
    Contains the Hero block and the Detailed Contacts block.
    """

    body = StreamField(
        [
            ("hero", HeroBlock(label=_("Блок героя"))),
            ("detailed_contacts", DetailedContactsBlock(label=_("Подробные контакты"))),
            (
                "text_content",
                blocks.RichTextBlock(
                    label=_("Текстовое содержание"),
                    features=["h2", "h3", "bold", "italic", "link", "ul", "ol"],
                ),
            ),
        ],
        use_json_field=True,
        verbose_name=_("Содержание страницы Контакты"),
    )
    max_count = 1
    content_panels = Page.content_panels + [FieldPanel("body")]
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = _("Страница контактов")
        verbose_name_plural = _("Страница контактов")

    def get_detailed_contacts_block(self):
        """
        Searches for the first 'detailed_contacts' block in the StreamField body.
        """
        for block in self.body:
            if block.block_type == "detailed_contacts":
                logger.debug(f"Found detailed_contacts block in page {self.id}")
                return block

        logger.warning(f"No detailed_contacts block found in page {self.id}")
        return None
