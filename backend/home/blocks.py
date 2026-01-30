"""home/blocks.py."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class HeroBlock(blocks.StructBlock):
    """Main hero banner block featuring a video background."""
    video = VideoChooserBlock(label="Фоновое видео")
    title = blocks.CharBlock(default="Орех Причерноморья")
    subtitle = blocks.TextBlock(required=False)
    link_url = blocks.URLBlock(required=False)

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/hero_block.html"


class ProductSectionBlock(blocks.StructBlock):
    """Block used to display a selection of products."""
    title = blocks.CharBlock(default="Продукция")
    description = blocks.TextBlock(required=False)
    featured_products = blocks.ListBlock(
        blocks.PageChooserBlock(target_model="shop.ProductPage"),
        label="Выберите товары"
    )
    shop_link = blocks.PageChooserBlock(required=False)

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/product_section.html"


class MediaGalleryBlock(blocks.StreamBlock):
    """Helper block for combining images and videos in a stream."""
    image = ImageChooserBlock()
    video = VideoChooserBlock()


class AboutBlock(blocks.StructBlock):
    """Block displaying information about the manufacturer."""
    title = blocks.CharBlock(default="О производителе")
    text = blocks.RichTextBlock()
    link = blocks.PageChooserBlock(required=False)
    gallery = MediaGalleryBlock()

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/about_block.html"


class StatItemBlock(blocks.StructBlock):
    """Represents a single statistical data point."""
    value = blocks.CharBlock()
    unit = blocks.CharBlock(required=False)
    description = blocks.CharBlock()


class StatsBlock(blocks.StructBlock):
    """Block for displaying a list of statistics."""
    stats = blocks.ListBlock(StatItemBlock())

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/stats_block.html"


class MissionBlock(blocks.StructBlock):
    """Block displaying the company mission with a video."""
    video = VideoChooserBlock()
    overlay_text = blocks.TextBlock()
    button_text = blocks.CharBlock(default="Смотреть видео")

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/mission_block.html"


class BenefitCardBlock(blocks.StructBlock):
    """Card block representing a specific benefit."""
    image = ImageChooserBlock()
    icon = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.TextBlock()


class BenefitsBlock(blocks.StructBlock):
    """Block containing a list of benefit cards."""
    cards = blocks.ListBlock(BenefitCardBlock())

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/benefits_block.html"


class EcoBannerBlock(blocks.StructBlock):
    """Banner block emphasizing eco-friendly production."""
    background_image = ImageChooserBlock()
    icon = ImageChooserBlock()
    title = blocks.CharBlock(default="Эко продукция")
    text = blocks.TextBlock()

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/eco_banner.html"


class LatestNewsBlock(blocks.StructBlock):
    """Block for displaying the latest news articles."""
    title = blocks.CharBlock(default="Новости")
    subtitle = blocks.TextBlock(required=False)
    count = blocks.IntegerBlock(default=3)
    news_index_page = blocks.PageChooserBlock(target_model="news.NewsIndexPage")

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/latest_news.html"


class ContactsMapBlock(blocks.StructBlock):
    """Block displaying contact details and an embedded map."""
    phones = blocks.ListBlock(blocks.CharBlock())
    email = blocks.EmailBlock()
    address_office = blocks.TextBlock()
    address_production = blocks.TextBlock()
    map_embed_code = blocks.RawHTMLBlock()

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "home/blocks/contacts_block.html"
