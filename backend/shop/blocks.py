"""shop/blocks.py"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

# pylint: disable=too-few-public-methods


class TabItemBlock(blocks.StructBlock):
    """
    Represents a single tab containing a title, optional image, and rich text content.
    """

    title = blocks.CharBlock(label=_("Заголовок таба"), required=True)
    image = ImageChooserBlock(label=_("Изображение"), required=False)
    image_alignment = blocks.ChoiceBlock(
        choices=[("left", _("Картинка слева")), ("right", _("Картинка справа"))],
        default="left",
        label=_("Расположение картинки"),
        required=False,
    )
    content = blocks.RichTextBlock(label=_("Текст"))

    class Meta:
        """
        Meta options for TabItemBlock.
        """

        label = _("Таб")


class ProductTabsBlock(blocks.StructBlock):
    """
    Block representing a section containing a list of tabs.
    """

    tabs = blocks.ListBlock(TabItemBlock(), label=_("Список табов"))

    class Meta:
        """
        Meta options for ProductTabsBlock.
        """

        template = "shop/blocks/product_tabs.html"
        icon = "list-ul"
        label = _("Секция с табами")
