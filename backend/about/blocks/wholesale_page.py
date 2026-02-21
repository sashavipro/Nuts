"""about/blocks/wholesale_page.py."""

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class WholesaleIntroBlock(blocks.StructBlock):
    """
    Introductory block: Title on the left, two text columns on the right.
    """

    title = blocks.CharBlock(label=_("Заголовок (слева)"))
    column_1 = blocks.RichTextBlock(
        label=_("Текст (правая часть, колонка 1)"),
        features=["h3", "h4", "bold", "italic", "ol", "ul", "link"],
    )
    column_2 = blocks.RichTextBlock(
        required=False,
        label=_("Текст (правая часть, колонка 2)"),
        features=["h3", "h4", "bold", "italic", "ol", "ul", "link"],
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "about/blocks/wholesale_intro.html"
        icon = "title"
        label = _("Интро (Заголовок + 2 колонки)")


class TabMiniItemBlock(blocks.StructBlock):
    """
    Mini-block inside tab content (Icon + Title + Description).
    Example: 'Cashless payment' + description.
    """

    # Выбор между иконкой-картинкой и иконочным шрифтом
    icon_type = blocks.ChoiceBlock(
        choices=[
            ("image", _("Картинка")),
            ("font", _("Иконочный шрифт")),
        ],
        default="image",
        label=_("Тип иконки"),
    )
    icon_image = ImageChooserBlock(required=False, label=_("Иконка (Картинка)"))
    icon_font_class = blocks.CharBlock(
        required=False,
        label=_("Класс иконки (Шрифт)"),
        help_text=_("Например: icons-delivery"),
    )
    title = blocks.CharBlock(label=_("Заголовок"))
    description = blocks.TextBlock(label=_("Описание"))

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        icon = "list-ul"
        label = _("Элемент с иконкой")


class TabItemBlock(blocks.StructBlock):
    """
    Represents a single tab: its label in the menu and its content area.
    """

    # НАВИГАЦИЯ (МЕНЮ ТАБОВ)
    tab_label = blocks.CharBlock(
        label=_("Название таба (в меню)"), help_text=_("Например: 'Безналичный расчет'")
    )

    tab_icon_type = blocks.ChoiceBlock(
        choices=[
            ("image", _("Картинка")),
            ("font", _("Иконочный шрифт")),
        ],
        default="font",
        label=_("Тип иконки таба"),
        required=False,
    )
    tab_icon_image = ImageChooserBlock(
        required=False, label=_("Иконка таба (Картинка)")
    )
    tab_icon_font_class = blocks.CharBlock(
        required=False,
        label=_("Класс иконки таба"),
        help_text=_("Например: icons-card"),
    )

    # КОНТЕНТ (ЛЕВАЯ ЧАСТЬ)
    title = blocks.CharBlock(
        label=_("Главный заголовок контента"),
        help_text=_("Например: Оплата банковскими картами (Без переплат)"),
        required=False,
    )

    # Комбинированный контент: иконки + текст ИЛИ просто текст
    content_items = blocks.StreamBlock(
        [
            ("icon_item", TabMiniItemBlock()),
            (
                "text_paragraph",
                blocks.RichTextBlock(
                    label=_("Текстовый абзац"),
                    features=["bold", "italic", "link"],
                    help_text=_("Простой текстовый абзац без иконки"),
                ),
            ),
        ],
        label=_("Содержимое (иконки + текст или просто текст)"),
        required=False,
    )

    # КНОПКА (опционально)
    button_text = blocks.CharBlock(
        required=False, label=_("Текст кнопки"), help_text=_("Например: 'Написать нам'")
    )
    button_url = blocks.URLBlock(
        required=False,
        label=_("URL кнопки"),
        help_text=_("Например: /contacts/ или https://example.com"),
    )

    # ПРАВАЯ ЧАСТЬ КОНТЕНТА
    image = ImageChooserBlock(label=_("Картинка справа"))

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        icon = "doc-full"
        label = _("Таб")


class WholesaleTabsBlock(blocks.StructBlock):
    """
    Section containing a set of tabs.
    """

    tabs = blocks.ListBlock(TabItemBlock(), label=_("Список табов"))

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "about/blocks/wholesale_tabs.html"
        icon = "folder-open-inverse"
        label = _("Секция табов (Оплата/Доставка)")
