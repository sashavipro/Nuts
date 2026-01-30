"""about/blocks/delivery_page.py."""

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ServiceMethodItemBlock(blocks.StructBlock):
    """Single item representing a service method (e.g., payment type)."""
    icon = ImageChooserBlock()
    title = blocks.CharBlock()
    description = blocks.TextBlock()


class TabContentBlock(blocks.StructBlock):
    """Content for a single tab in the delivery/payment section."""
    tab_name = blocks.CharBlock()
    tab_icon = ImageChooserBlock()
    items = blocks.ListBlock(ServiceMethodItemBlock())
    image = ImageChooserBlock()


class PaymentDeliveryTabsBlock(blocks.StructBlock):
    """Container block for payment and delivery tabs."""
    tabs = blocks.ListBlock(TabContentBlock())
