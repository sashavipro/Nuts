"""about/blocks/wholesale_page.py."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ClientCategoryItemBlock(blocks.StructBlock):
    """Block representing a category of clients (e.g., Horeca, Retail)."""
    icon = ImageChooserBlock()
    title = blocks.CharBlock()


class WholesaleIntroBlock(blocks.StructBlock):
    """Introductory block for the wholesale page with client categories."""
    title = blocks.CharBlock()
    column_1 = blocks.TextBlock()
    column_2 = blocks.TextBlock()
    categories = blocks.ListBlock(ClientCategoryItemBlock())


class TextImageBlock(blocks.StructBlock):
    """Generic block with text and an image."""
    text = blocks.RichTextBlock()
    button_text = blocks.CharBlock()
    button_url = blocks.URLBlock()
    image = ImageChooserBlock()
    image_position = blocks.ChoiceBlock(
        choices=[('left', 'Left'), ('right', 'Right')],
        default='right'
    )
