"""news/blocks.py."""

import logging
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock
from contacts.blocks import SocialLinkBlock

logger = logging.getLogger(__name__)


class MediaOverlayBlock(blocks.StructBlock):
    """
    Block used in News content to display an image or video with optional overlay text.
    """

    image = ImageChooserBlock(required=False, label="Image")
    video = VideoChooserBlock(required=False, label="Video")

    overlay_text = blocks.RichTextBlock(
        required=False,
        label="Text over media",
        features=["h2", "h3", "h4", "bold", "italic", "link"],
        help_text="This text will be displayed over the image or video.",
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "news/blocks/media_overlay_block.html"
        icon = "media"
        label = "Media with Text"


class SidebarSocialBlock(blocks.StructBlock):
    """
    Sidebar widget block containing a title, subtitle, and social media links.
    """

    title = blocks.CharBlock(label="Title", default="Join Us")
    subtitle = blocks.TextBlock(label="Subtitle", required=False)
    socials = blocks.ListBlock(SocialLinkBlock(), label="Social Networks")

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "news/blocks/sidebar_social_block.html"
        icon = "group"
        label = "Sidebar Social Widget"
