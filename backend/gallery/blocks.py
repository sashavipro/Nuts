"""gallery/blocks.py"""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class GalleryHeroBlock(blocks.StructBlock):
    """Video or large banner inside the gallery."""

    video = VideoChooserBlock(required=False, label=_("Видео (приоритет)"))
    image = ImageChooserBlock(required=False, label=_("Картинка"))
    title = blocks.CharBlock(required=False, label=_("Заголовок"))
    subtitle = blocks.TextBlock(required=False, label=_("Подзаголовок"))
    size = blocks.ChoiceBlock(
        choices=[("col-12", _("100%")), ("col-lg-6", _("50%")), ("col-lg-4", _("33%"))],
        default="col-12",
        label=_("Размер"),
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "gallery/blocks/gallery_hero_block.html"
        icon = "media"
        label = _("Видео/Баннер")


class GalleryCardBlock(blocks.StructBlock):
    """Card with hover effect."""

    image = ImageChooserBlock(label=_("Фоновая картинка"))
    icon = ImageChooserBlock(required=False, label=_("Иконка"))
    title = blocks.CharBlock(required=False, label=_("Заголовок"))
    description = blocks.TextBlock(required=False, label=_("Текст"))
    size = blocks.ChoiceBlock(
        choices=[
            ("col-lg-4", _("33%")),
            ("col-lg-6", _("50%")),
            ("col-lg-3", _("25%")),
        ],
        default="col-lg-4",
        label=_("Размер"),
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "gallery/blocks/gallery_card_block.html"
        icon = "image"
        label = _("Карточка")


class GallerySectionBlock(blocks.StructBlock):
    """
    Container block. Contains the section title and a list of elements.
    """

    title = blocks.CharBlock(default=_("Наша галерея"), label=_("Заголовок секции"))
    description = blocks.TextBlock(required=False, label=_("Описание секции"))

    items_per_page = blocks.IntegerBlock(
        default=6,
        label=_("Элементов на странице (для пагинации)"),
        help_text=_(
            "Сколько карточек показывать за раз. Работает только на детальной странице галереи."
        ),
    )

    items = blocks.StreamBlock(
        [
            ("gallery_hero", GalleryHeroBlock()),
            ("gallery_card", GalleryCardBlock()),
        ],
        label=_("Элементы галереи"),
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "gallery/blocks/gallery_section.html"
        icon = "images"
        label = _("Секция: Галерея")
