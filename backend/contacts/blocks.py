"""contacts/blocks.py."""

import logging
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

logger = logging.getLogger(__name__)


class BaseIconBlock(blocks.StructBlock):
    """
    Abstract base block containing fields for icon selection.

    Allows choosing between an uploaded image or a font icon class.
    Inherit from this block to add icon functionality to other blocks.
    """

    icon_type = blocks.ChoiceBlock(
        choices=[
            ("image", _("Изображение")),
            ("font", _("Шрифт Иконка")),
        ],
        default="font",
        label=_("Тип значка"),
        required=False,
    )
    icon_image = ImageChooserBlock(required=False, label=_("Иконка (изображение)"))
    icon_font_class = blocks.CharBlock(
        required=False,
        label=_("Класс Icon"),
        help_text=_("Пример: icons-phone, icons-post, icons-home"),
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        abstract = True


class SocialLinkBlock(BaseIconBlock):
    """
    Block representing a single social media link.
    Contains an icon and a URL.
    """

    link = blocks.URLBlock(label=_("Ссылка"), required=False)

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        icon = "link"
        label = _("Социальная связь")


class PhoneSectionBlock(BaseIconBlock):
    """
    Section block for displaying phone numbers and associated social links.
    """

    phones = blocks.ListBlock(
        blocks.CharBlock(label=_("Номер телефона")),
        label=_("Список телефонов"),
        required=False,
    )
    socials = blocks.ListBlock(
        SocialLinkBlock(), label=_("Социальные сети"), required=False
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        label = _("Раздел Телефон")
        icon = "mobile-alt"


class EmailSectionBlock(BaseIconBlock):
    """
    Section block for displaying email addresses.
    """

    emails = blocks.ListBlock(
        blocks.EmailBlock(label=_("Адрес электронной почты")),
        label=_("Список адресов электронной почты"),
        required=False,
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        label = _("Раздел Электронная почта")
        icon = "mail"


class AddressItemBlock(blocks.StructBlock):
    """
    Block representing a single physical address.
    """

    title = blocks.CharBlock(label=_("Филиал/Название"), required=False)
    text = blocks.RichTextBlock(
        label=_("Текст адреса"),
        features=["bold", "italic", "link", "br"],
        required=True,
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        label = _("Адрес")
        icon = "home"


class DetailedContactsBlock(blocks.StructBlock):
    """
    Main structural block for the Contact Page.
    Aggregates phone, email, address sections, and a map embed.
    """

    main_title = blocks.CharBlock(
        default=_("Контакты"), label=_("Основное название"), required=False
    )

    phone_section = PhoneSectionBlock(
        label=_("Телефоны и социальные сети"), required=False
    )
    email_section = EmailSectionBlock(
        label=_("Блокировка электронной почты"), required=False
    )

    addresses = blocks.ListBlock(
        AddressItemBlock(), label=_("Список адресов"), required=False
    )

    map_embed = blocks.RawHTMLBlock(
        label=_("Код для вставки карты (iframe Google Maps)"), required=False
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "contacts/blocks/detailed_contacts.html"
        icon = "map"
        label = _("Подробные контакты")


class ContactImportBlock(blocks.StructBlock):
    """
    Block for importing a contact section from an existing ContactPage.
    Useful for displaying contact info in footers or other pages.
    """

    contact_page = blocks.PageChooserBlock(
        target_model="contacts.ContactPage",
        label=_("Выберите страницу Контакты"),
        required=True,
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "contacts/blocks/contact_import_wrapper.html"
        icon = "link"
        label = _("Импорт контактов")
