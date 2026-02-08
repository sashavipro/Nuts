"""about/blocks/wholesale_page.py."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class WholesaleIntroBlock(blocks.StructBlock):
    """
    Introductory block: Title on the left, two text columns on the right.
    """

    title = blocks.CharBlock(label="Заголовок (слева)")
    column_1 = blocks.RichTextBlock(
        label="Текст (правая часть, колонка 1)",
        features=["h3", "h4", "bold", "italic", "ol", "ul", "link"],
    )
    column_2 = blocks.RichTextBlock(
        required=False,
        label="Текст (правая часть, колонка 2)",
        features=["h3", "h4", "bold", "italic", "ol", "ul", "link"],
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "about/blocks/wholesale_intro.html"
        icon = "title"
        label = "Интро (Заголовок + 2 колонки)"


class TabMiniItemBlock(blocks.StructBlock):
    """
    Mini-block inside tab content (Icon + Title + Description).
    Example: 'Cashless payment' + description.
    """

    # Выбор между иконкой-картинкой и иконочным шрифтом
    icon_type = blocks.ChoiceBlock(
        choices=[
            ("image", "Картинка"),
            ("font", "Иконочный шрифт"),
        ],
        default="image",
        label="Тип иконки",
    )
    icon_image = ImageChooserBlock(required=False, label="Иконка (картинка)")
    icon_font_class = blocks.CharBlock(
        required=False,
        label="Класс иконки (например: icons-vector12)",
        help_text=(
            "Используйте классы из шрифта 'nut'. "
            "Например: icons-vector12, icons-credit-card и т.д."
        ),
    )

    title = blocks.CharBlock(label="Название пункта")
    description = blocks.TextBlock(required=False, label="Описание")

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        icon = "tick-inverse"


class TabItemBlock(blocks.StructBlock):
    """
    A single tab item.
    Tab button settings + Content (Left part and Right image).
    """

    # Настройки самой кнопки переключения
    tab_label = blocks.CharBlock(label="Название таба (напр. Оплата заказа)")

    # Выбор между иконкой-картинкой и иконочным шрифтом для ТАБА
    tab_icon_type = blocks.ChoiceBlock(
        choices=[
            ("image", "Картинка"),
            ("font", "Иконочный шрифт"),
        ],
        default="font",
        label="Тип иконки таба",
    )
    tab_icon_image = ImageChooserBlock(required=False, label="Иконка таба (картинка)")
    tab_icon_font_class = blocks.CharBlock(
        required=False,
        label="Класс иконки таба (например: icons-credit-card)",
        help_text="Используйте классы из шрифта 'nut'",
    )

    # ЛЕВАЯ ЧАСТЬ КОНТЕНТА
    content_title = blocks.CharBlock(
        label="Заголовок контента (напр. Способы оплаты)", required=False
    )

    # Комбинированный контент: иконки + текст ИЛИ просто текст
    content_items = blocks.StreamBlock(
        [
            ("icon_item", TabMiniItemBlock()),
            (
                "text_paragraph",
                blocks.RichTextBlock(
                    label="Текстовый абзац",
                    features=["bold", "italic", "link"],
                    help_text="Простой текстовый абзац без иконки",
                ),
            ),
        ],
        label="Содержимое (иконки + текст или просто текст)",
        required=False,
    )

    # КНОПКА (опционально)
    button_text = blocks.CharBlock(
        required=False, label="Текст кнопки", help_text="Например: 'Написать нам'"
    )
    button_url = blocks.URLBlock(
        required=False,
        label="URL кнопки",
        help_text="Например: /contacts/ или https://example.com",
    )

    # ПРАВАЯ ЧАСТЬ КОНТЕНТА
    image = ImageChooserBlock(label="Картинка справа")

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        icon = "doc-full"
        label = "Таб"


class WholesaleTabsBlock(blocks.StructBlock):
    """
    Section containing a set of tabs.
    """

    tabs = blocks.ListBlock(TabItemBlock(), label="Список табов")

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "about/blocks/wholesale_tabs.html"
        icon = "list-ul"
        label = "Секция Табов (Оплата/Доставка/Возврат)"
