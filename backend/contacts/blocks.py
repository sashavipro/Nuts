"""contacts/blocks.py."""

import logging
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
            ("image", "Image"),
            ("font", "Font Icon"),
        ],
        default="font",
        label="Icon Type",
        required=False,
    )
    icon_image = ImageChooserBlock(required=False, label="Icon (Image)")
    icon_font_class = blocks.CharBlock(
        required=False,
        label="Icon Class",
        help_text="Example: icons-phone, icons-post, icons-home",
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        abstract = True


class SocialLinkBlock(BaseIconBlock):
    """
    Block representing a single social media link.
    Contains an icon and a URL.
    """

    link = blocks.URLBlock(label="Link", required=False)

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        icon = "link"
        label = "Social Link"


class PhoneSectionBlock(BaseIconBlock):
    """
    Section block for displaying phone numbers and associated social links.
    """

    phones = blocks.ListBlock(
        blocks.CharBlock(label="Phone Number", required=False),
        label="Phone List",
        required=False,
    )
    socials = blocks.ListBlock(
        SocialLinkBlock(), label="Social Buttons (WhatsApp, Telegram)", required=False
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        label = "Phones Section"
        icon = "mobile-alt"


class EmailSectionBlock(BaseIconBlock):
    """
    Section block for displaying an email address with an icon.
    """

    email = blocks.EmailBlock(label="Email", required=False)

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        label = "Email Section"
        icon = "mail"


class AddressItemBlock(BaseIconBlock):
    """
    Block representing a single physical address location.
    Contains a title, rich text description, and an icon.
    """

    title = blocks.CharBlock(label="Title (e.g. Office)", required=False)
    text = blocks.RichTextBlock(
        label="Address Text", features=["bold", "italic", "link"], required=False
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        label = "Address"
        icon = "home"


class DetailedContactsBlock(blocks.StructBlock):
    """
    Main structural block for the Contact Page.
    Aggregates phone, email, address sections, and a map embed.
    """

    main_title = blocks.CharBlock(
        default="Contacts", label="Main Title", required=False
    )

    phone_section = PhoneSectionBlock(label="Phones & Socials Block", required=False)
    email_section = EmailSectionBlock(label="Email Block", required=False)

    addresses = blocks.ListBlock(
        AddressItemBlock(), label="Address List", required=False
    )

    map_embed = blocks.RawHTMLBlock(
        label="Map Embed Code (Google Maps iframe)", required=False
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "contacts/blocks/detailed_contacts.html"
        icon = "map"
        label = "Detailed Contacts"


class ContactImportBlock(blocks.StructBlock):
    """
    Block for importing a contact section from an existing ContactPage.
    Useful for displaying contact info in footers or other pages.
    """

    contact_page = blocks.PageChooserBlock(
        target_model="contacts.ContactPage", label="Choose Contact Page", required=True
    )

    class Meta:  # pylint: disable=too-few-public-methods, missing-class-docstring
        template = "contacts/blocks/contact_import_wrapper.html"
        icon = "link"
        label = "Import Contacts"
