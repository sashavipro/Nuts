"""home/blocks.py."""

from django.apps import apps
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class HeroBlock(blocks.StructBlock):
    """Main hero banner block featuring a video background or an image."""

    video = VideoChooserBlock(required=False, label="Видео")
    image = ImageChooserBlock(required=False, label="Фоновая картинка (если нет видео)")

    title = blocks.CharBlock(required=False, default="Орех Причерноморья")
    subtitle = blocks.TextBlock(required=False)

    button_text = blocks.CharBlock(required=False, default="Смотреть видео")

    class Meta:
        template = "home/blocks/hero_block.html"


class MediaGalleryBlock(blocks.StreamBlock):
    """Helper block for combining images and videos in a stream."""

    image = ImageChooserBlock()
    video = VideoChooserBlock()


class AboutBlock(blocks.StructBlock):
    """Block displaying information about the manufacturer."""

    title = blocks.CharBlock(default="О производителе")
    text = blocks.RichTextBlock(
        features=["h3", "h4", "bold", "italic", "ol", "ul", "hr", "link"]
    )
    link = blocks.PageChooserBlock(required=False)
    gallery = MediaGalleryBlock()

    class Meta:
        template = "home/blocks/about_block.html"


class StatItemBlock(blocks.StructBlock):
    """Represents a single statistical data point."""

    value = blocks.CharBlock()
    unit = blocks.CharBlock(required=False)
    description = blocks.CharBlock()


class StatsBlock(blocks.StructBlock):
    """Block for displaying a list of statistics."""

    stats = blocks.ListBlock(StatItemBlock())

    class Meta:
        template = "home/blocks/stats_block.html"


class BenefitCardBlock(blocks.StructBlock):
    """Card block representing a specific benefit."""

    image = ImageChooserBlock()
    icon = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.TextBlock()


class BenefitsBlock(blocks.StructBlock):
    """Block containing a list of benefit cards."""

    cards = blocks.ListBlock(BenefitCardBlock())

    class Meta:
        template = "home/blocks/benefits_block.html"


class EcoBannerBlock(blocks.StructBlock):
    """Banner block emphasizing eco-friendly production."""

    background_image = ImageChooserBlock()
    icon = ImageChooserBlock()
    title = blocks.CharBlock(default="Эко продукция")
    text = blocks.TextBlock()

    class Meta:
        template = "home/blocks/eco_banner.html"


class LatestNewsBlock(blocks.StructBlock):
    """Block for displaying the latest news articles."""

    title = blocks.CharBlock(default="Новости")
    subtitle = blocks.TextBlock(required=False)
    count = blocks.IntegerBlock(default=3)

    news_index_page = blocks.PageChooserBlock(
        target_model="news.NewsIndexPage", required=False
    )

    class Meta:
        template = "home/blocks/latest_news.html"
        icon = "doc-full"
        label = "Слайдер последних новостей"

    def get_context(self, value, parent_context=None):
        """
        The method retrieves data from the database before sending it to the template.
        """
        # Resolve Cyclic Import: Use get_model instead of direct import
        NewsPage = apps.get_model("news", "NewsPage")

        context = super().get_context(value, parent_context=parent_context)

        index_page = value.get("news_index_page")
        count = value.get("count", 3)

        if index_page:
            news_items = (
                NewsPage.objects.live().child_of(index_page).order_by("-date")[:count]
            )
        else:
            news_items = NewsPage.objects.live().order_by("-date")[:count]

        context["news_items"] = news_items
        return context
