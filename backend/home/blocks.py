"""home/blocks.py."""

from django.apps import apps
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock

# pylint: disable=too-few-public-methods


class HeroBlock(blocks.StructBlock):
    """Main hero banner block featuring a video background or an image."""

    video = VideoChooserBlock(required=False, label=_("Видео"))
    image = ImageChooserBlock(
        required=False, label=_("Фоновая картинка (если нет видео)")
    )

    title = blocks.CharBlock(
        required=False, default=_("Орех Причерноморья"), label=_("Заголовок")
    )
    subtitle = blocks.TextBlock(required=False, label=_("Подзаголовок"))

    button_text = blocks.CharBlock(
        required=False, default=_("Смотреть видео"), label=_("Текст кнопки")
    )

    class Meta:
        """Meta options for HeroBlock."""

        template = "home/blocks/hero_block.html"
        label = _("Главный экран (Hero)")


class MediaGalleryBlock(blocks.StreamBlock):
    """Helper block for combining images and videos in a stream."""

    image = ImageChooserBlock(label=_("Изображение"))
    video = VideoChooserBlock(label=_("Видео"))

    class Meta:
        """Meta options for MediaGalleryBlock."""

        label = _("Медиа галерея")


class AboutBlock(blocks.StructBlock):
    """Block displaying information about the manufacturer."""

    title = blocks.CharBlock(default=_("О производителе"), label=_("Заголовок"))
    text = blocks.RichTextBlock(
        features=["h3", "h4", "bold", "italic", "ol", "ul", "hr", "link"],
        label=_("Текст"),
    )
    link = blocks.PageChooserBlock(required=False, label=_("Ссылка на страницу"))
    gallery = MediaGalleryBlock(label=_("Галерея (Слайдер)"))

    class Meta:
        """Meta options for AboutBlock."""

        template = "home/blocks/about_block.html"
        label = _("Блок 'О производителе'")


class StatItemBlock(blocks.StructBlock):
    """Represents a single statistical data point."""

    value = blocks.CharBlock(label=_("Значение (цифра)"))
    unit = blocks.CharBlock(required=False, label=_("Единица измерения"))
    description = blocks.CharBlock(label=_("Описание"))

    class Meta:
        """Meta options for StatItemBlock."""

        label = _("Элемент статистики")


class StatsBlock(blocks.StructBlock):
    """Block for displaying a list of statistics."""

    stats = blocks.ListBlock(StatItemBlock(), label=_("Список статистики"))

    class Meta:
        """Meta options for StatsBlock."""

        template = "home/blocks/stats_block.html"
        label = _("Блок статистики")


class BenefitCardBlock(blocks.StructBlock):
    """Card block representing a specific benefit."""

    image = ImageChooserBlock(label=_("Фоновое изображение"))
    icon = ImageChooserBlock(label=_("Иконка"))
    title = blocks.CharBlock(label=_("Заголовок"))
    description = blocks.TextBlock(label=_("Описание"))

    class Meta:
        """Meta options for BenefitCardBlock."""

        label = _("Карточка преимущества")


class BenefitsBlock(blocks.StructBlock):
    """Block containing a list of benefit cards."""

    title = blocks.CharBlock(label=_("Заголовок блока"), required=False)
    description = blocks.TextBlock(label=_("Описание блока"), required=False)
    cards = blocks.ListBlock(BenefitCardBlock(), label=_("Карточки преимуществ"))

    class Meta:
        """Meta options for BenefitsBlock."""

        template = "home/blocks/benefits_block.html"
        label = _("Блок преимуществ")


class EcoBannerBlock(blocks.StructBlock):
    """Banner block emphasizing eco-friendly production."""

    background_image = ImageChooserBlock(required=False, label=_("Фоновое изображение"))
    icon = ImageChooserBlock(required=False, label=_("Иконка"))
    title = blocks.CharBlock(default=_("Эко продукция"), label=_("Заголовок"))
    text = blocks.TextBlock(label=_("Текст"))

    class Meta:
        """Meta options for EcoBannerBlock."""

        template = "home/blocks/eco_banner.html"
        label = _("Эко баннер")


class LatestNewsBlock(blocks.StructBlock):
    """Block for displaying the latest news articles."""

    title = blocks.CharBlock(default=_("Новости"), label=_("Заголовок"))
    subtitle = blocks.TextBlock(required=False, label=_("Подзаголовок"))
    count = blocks.IntegerBlock(default=3, label=_("Количество новостей"))

    news_index_page = blocks.PageChooserBlock(
        target_model="news.NewsIndexPage",
        required=False,
        label=_("Страница новостей (для кнопки 'Все новости')"),
    )

    class Meta:
        """Meta options for LatestNewsBlock."""

        template = "home/blocks/latest_news.html"
        icon = "doc-full"
        label = _("Слайдер последних новостей")

    def get_context(self, value, parent_context=None):
        """
        The method retrieves data from the database before sending it to the template.
        """
        # Resolve Cyclic Import: Use get_model instead of direct import
        news_page_model = apps.get_model("news", "NewsPage")

        context = super().get_context(value, parent_context=parent_context)

        index_page = value.get("news_index_page")
        count = value.get("count", 3)

        if index_page:
            news_items = (
                news_page_model.objects.live()
                .child_of(index_page)
                .order_by("-date")[:count]
            )
        else:
            news_items = news_page_model.objects.live().order_by("-date")[:count]

        context["news_items"] = news_items
        return context


class FeaturedProductsBlock(blocks.StructBlock):
    """Block for displaying products from the store on other pages."""

    title = blocks.CharBlock(default=_("Продукция"), label=_("Заголовок"))
    description = blocks.TextBlock(required=False, label=_("Описание"))
    count = blocks.IntegerBlock(default=3, label=_("Количество товаров"))

    class Meta:
        """Meta options for FeaturedProductsBlock."""

        template = "home/blocks/featured_products.html"
        icon = "pick"
        label = _("Блок товаров")

    def get_context(self, value, parent_context=None):
        """Get products from the database before rendering."""
        context = super().get_context(value, parent_context=parent_context)

        product = apps.get_model("shop", "Product")

        count = value.get("count", 3)
        products = product.objects.filter(live=True).order_by("-created_at")[:count]

        context["products"] = products
        return context
