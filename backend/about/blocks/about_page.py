"""about/blocks/about_page.py."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class FounderHistoryBlock(blocks.StructBlock):
    """Block displaying founder information and company history."""

    founder_image = ImageChooserBlock(required=False)
    founder_name = blocks.CharBlock(required=False)
    founder_role = blocks.CharBlock(required=False, label="Должность")
    quote = blocks.TextBlock(required=False, label="Цитата")
    button_text = blocks.CharBlock(required=False)
    button_url = blocks.URLBlock(required=False)

    history_title = blocks.CharBlock(required=False, default="История предприятия")
    history_text = blocks.RichTextBlock(required=False)
    history_bg_image = ImageChooserBlock(required=False)

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "about/blocks/founder_history_block.html"
