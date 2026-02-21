"""about/blocks/about_page.py."""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class FounderHistoryBlock(blocks.StructBlock):
    """Block displaying founder information and company history."""

    founder_image = ImageChooserBlock(required=False, label=_("Изображение основателя"))
    founder_name = blocks.CharBlock(required=False, label=_("Имя основателя"))
    founder_role = blocks.CharBlock(required=False, label=_("Должность"))
    quote = blocks.TextBlock(required=False, label=_("Цитата"))
    button_text = blocks.CharBlock(required=False, label=_("Текст кнопки"))
    button_url = blocks.URLBlock(required=False, label=_("Ссылка кнопки"))

    history_title = blocks.CharBlock(
        required=False, default=_("История предприятия"), label=_("Заголовок истории")
    )
    history_text = blocks.RichTextBlock(required=False, label=_("Текст истории"))
    history_bg_image = ImageChooserBlock(
        required=False, label=_("Фоновое изображение истории")
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "about/blocks/founder_history_block.html"
        label = _("Блок истории и основателя")
