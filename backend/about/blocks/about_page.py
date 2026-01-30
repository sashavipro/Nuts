"""about/blocks/about_page.py."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class ImageBannerBlock(blocks.StructBlock):
    """Banner block with optional background video and link."""
    video = VideoChooserBlock(label="Фоновое видео", required=False)
    title = blocks.CharBlock()
    subtitle = blocks.TextBlock(required=False)
    video_url = blocks.URLBlock(required=False, label="Ссылка на видео (кнопка Play)")


class FounderHistoryBlock(blocks.StructBlock):
    """Block displaying founder information and company history."""
    founder_image = ImageChooserBlock()
    founder_name = blocks.CharBlock()
    founder_role = blocks.CharBlock(label="Должность")
    quote = blocks.TextBlock(label="Цитата")
    button_text = blocks.CharBlock(required=False)
    button_url = blocks.URLBlock(required=False)

    history_title = blocks.CharBlock(default="История предприятия")
    history_text = blocks.RichTextBlock()
    history_bg_image = ImageChooserBlock(required=False)


class SimpleGalleryBlock(blocks.StructBlock):
    """Simple grid gallery block."""
    title = blocks.CharBlock()
    description = blocks.TextBlock(required=False)
    items = blocks.ListBlock(
        blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('video', VideoChooserBlock(required=False)),
        ]), label="Элементы галереи"
    )
    view_all_link = blocks.URLBlock(required=False)
