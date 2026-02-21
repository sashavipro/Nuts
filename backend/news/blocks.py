"""news/blocks.py."""

import logging
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock
from contacts.blocks import SocialLinkBlock

logger = logging.getLogger(__name__)


class MediaOverlayBlock(blocks.StructBlock):
    """
    Block used in News content to display an image or video with optional overlay text.
    """

    image = ImageChooserBlock(required=False, label=_("Изображение"))
    video = VideoChooserBlock(required=False, label=_("Видео"))

    overlay_text = blocks.RichTextBlock(
        required=False,
        label=_("Текст над медиа"),
        features=["h2", "h3", "h4", "bold", "italic", "link"],
        help_text=_("Этот текст будет отображаться поверх изображения или видео."),
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "news/blocks/media_overlay_block.html"
        icon = "media"
        label = _("Медиа с текстом")


class SidebarSocialBlock(blocks.StructBlock):
    """
    Sidebar widget block containing a title, subtitle, and social media links.
    """

    title = blocks.CharBlock(label=_("Название"), default=_("Присоединяйтесь к нам"))
    subtitle = blocks.TextBlock(label=_("Подзаголовок"), required=False)
    socials = blocks.ListBlock(SocialLinkBlock(), label=_("Социальные сети"))

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "news/blocks/sidebar_social_block.html"
        icon = "group"
        label = _("Виджет социальной сети в боковой панели")
