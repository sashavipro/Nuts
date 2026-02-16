"""gallery/blocks.py"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmedia.blocks import VideoChooserBlock


class GalleryHeroBlock(blocks.StructBlock):
    """Video or large banner inside the gallery."""

    video = VideoChooserBlock(required=False, label="Видео (приоритет)")
    image = ImageChooserBlock(required=False, label="Картинка")
    title = blocks.CharBlock(required=False, label="Заголовок")
    subtitle = blocks.TextBlock(required=False, label="Подзаголовок")
    size = blocks.ChoiceBlock(
        choices=[("col-12", "100%"), ("col-lg-6", "50%"), ("col-lg-4", "33%")],
        default="col-12",
        label="Размер",
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "gallery/blocks/gallery_hero_block.html"
        icon = "media"
        label = "Видео/Баннер"


class GalleryCardBlock(blocks.StructBlock):
    """Card with hover effect."""

    image = ImageChooserBlock(label="Фоновая картинка")
    icon = ImageChooserBlock(required=False, label="Иконка")
    title = blocks.CharBlock(required=False, label="Заголовок")
    description = blocks.TextBlock(required=False, label="Текст")
    size = blocks.ChoiceBlock(
        choices=[("col-lg-4", "33%"), ("col-lg-6", "50%"), ("col-lg-3", "25%")],
        default="col-lg-4",
        label="Размер",
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "gallery/blocks/gallery_card_block.html"
        icon = "image"
        label = "Карточка"


class GallerySectionBlock(blocks.StructBlock):
    """
    Container block. Contains the section title and a list of elements.
    """

    title = blocks.CharBlock(default="Наша галерея", label="Заголовок секции")
    description = blocks.TextBlock(required=False, label="Описание секции")

    items_per_page = blocks.IntegerBlock(
        default=6,
        label="Элементов на странице (для пагинации)",
        help_text="Сколько карточек показывать за раз."
        " Работает только на детальной странице галереи.",
    )

    items = blocks.StreamBlock(
        [
            ("gallery_hero", GalleryHeroBlock()),
            ("gallery_card", GalleryCardBlock()),
        ],
        label="Элементы галереи",
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "gallery/blocks/gallery_section.html"
        icon = "folder-open-inverse"
        label = "Секция Галереи (Сетка)"
