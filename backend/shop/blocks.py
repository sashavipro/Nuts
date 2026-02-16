"""shop/blocks.py"""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class SkuBlock(blocks.StructBlock):
    """
    Block for displaying the product Stock Keeping Unit (SKU).
    """

    label = blocks.CharBlock(label="Текст (например: Артикул)", default="Артикул")

    class Meta:
        """
        Meta options for SkuBlock.
        """

        template = "shop/blocks/product_sku.html"
        icon = "tag"
        label = "Артикул (из базы)"


class ProductAttributeBlock(blocks.StructBlock):
    """
    Block for displaying a specific attribute from the Product model.
    Allows selection of composition, weight, energy value, etc.
    """

    label = blocks.CharBlock(
        label="Название характеристики", help_text="Например: Состав"
    )
    attribute_type = blocks.ChoiceBlock(
        choices=[
            ("composition", "Состав"),
            ("weight", "Вес (строка)"),
            ("energy_value", "Энергетическая ценность"),
            ("shelf_life", "Срок годности"),
            ("packaging", "Упаковка"),
        ],
        label="Что вывести из базы?",
    )

    class Meta:
        """
        Meta options for ProductAttributeBlock.
        """

        template = "shop/blocks/product_attribute.html"
        icon = "list-ul"
        label = "Характеристика товара"


class IconTextBlock(blocks.StructBlock):
    """
    Block for displaying an icon (image or CSS class) alongside text.
    """

    icon_image = ImageChooserBlock(required=False, label="Картинка иконки")
    # Or use a font class if you have an icon font
    icon_class = blocks.CharBlock(
        required=False,
        label="CSS класс иконки (если нет картинки)",
        help_text="Например: nut-icon icons-truck",
    )
    text = blocks.TextBlock(label="Текст")

    class Meta:
        """
        Meta options for IconTextBlock.
        """

        template = "shop/blocks/icon_text.html"
        icon = "image"
        label = "Иконка + Текст"


class PriceBlock(blocks.StructBlock):
    """
    Block for displaying the product price.
    """

    label = blocks.CharBlock(label="Текст (например: Ваша цена)", default="Цена")

    class Meta:
        """
        Meta options for PriceBlock.
        """

        template = "shop/blocks/product_price.html"
        icon = "cogs"  # or any other
        label = "Цена (из базы)"


class TabItemBlock(blocks.StructBlock):
    """
    Represents a single tab containing a title, optional image, and rich text content.
    """

    title = blocks.CharBlock(label="Заголовок таба", required=True)
    image = ImageChooserBlock(label="Изображение", required=False)
    image_alignment = blocks.ChoiceBlock(
        choices=[("left", "Картинка слева"), ("right", "Картинка справа")],
        default="left",
        label="Расположение картинки",
        required=False,
    )
    content = blocks.RichTextBlock(label="Текст")

    class Meta:
        """
        Meta options for TabItemBlock.
        """

        label = "Таб"


class ProductTabsBlock(blocks.StructBlock):
    """
    Block representing a section containing a list of tabs.
    """

    tabs = blocks.ListBlock(TabItemBlock(), label="Список табов")

    class Meta:
        """
        Meta options for ProductTabsBlock.
        """

        template = "shop/blocks/product_tabs.html"
        icon = "list-ul"
        label = "Секция с табами"
