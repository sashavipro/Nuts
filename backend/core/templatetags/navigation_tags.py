"""core/templatetags/navigation_tags.py."""

import logging
from django import template
from wagtail.models import Page, Site, Locale
from shop.models import ShopIndexPage, CartPage
from users.models import ProfilePage

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """
    Returns the root page of the current site corresponding to
    the currently active language (Locale).
    """
    request = context.get("request")
    if not request:
        logger.warning("Request missing in context for get_site_root.")
        return None

    site = Site.find_for_request(request)
    if not site:
        logger.warning("Site not found for request in get_site_root.")
        return None

    root_page = site.root_page

    current_locale = Locale.get_active()

    if root_page.locale == current_locale:
        return root_page

    translated_root = root_page.get_translation_or_none(current_locale)

    return translated_root or root_page


@register.simple_tag(takes_context=True)
def get_top_menu(context):
    """
    Returns the menu items (child pages of the localized root)
    that are live and marked 'Show in menus'.
    """
    site_root = get_site_root(context)

    if not site_root:
        return []

    return site_root.get_children().live().in_menu()


@register.inclusion_tag("includes/breadcrumbs.html", takes_context=True)
def breadcrumbs(context, is_hero=False):
    """
    Renders breadcrumbs for the current page.
    Excludes the root page and checks page depth.
    """
    page = context.get("page")

    if not isinstance(page, Page) or page.depth <= 2:
        ancestors = []
    else:
        ancestors = Page.objects.ancestor_of(page, inclusive=True).filter(depth__gt=1)

    return {
        "ancestors": ancestors,
        "request": context.get("request"),
        "is_hero": is_hero,
    }


@register.simple_tag(takes_context=True)
def has_hero_block(context):
    """
    Checks if the 'hero' block is present in the page's body streamfield.
    """
    page = context.get("page")
    if not page or not hasattr(page, "body"):
        return False

    for block in page.body:
        if block.block_type == "hero":
            return True
    return False


@register.simple_tag(takes_context=True)
def get_shop_url(context):
    """
    Returns the current URL of the store page for the current language.
    Searches for the page by its type (ShopIndexPage), so the link always works,
    even if the slug changes or the page is hidden from the menu.
    """
    request = context.get("request")
    current_locale = Locale.get_active()

    shop_page = ShopIndexPage.objects.filter(live=True, locale=current_locale).first()

    if not shop_page:
        shop_page = ShopIndexPage.objects.filter(live=True).first()

    if shop_page and request:
        return shop_page.get_url(request)

    return "/"


@register.simple_tag(takes_context=True)
def get_cart_url(context):
    """Returns the current URL of the shopping cart page for the current language."""
    request = context.get("request")
    current_locale = Locale.get_active()

    cart_page = CartPage.objects.filter(live=True, locale=current_locale).first()

    if not cart_page:
        cart_page = CartPage.objects.filter(live=True).first()

    if cart_page and request:
        return cart_page.get_url(request)

    return "/"


@register.simple_tag(takes_context=True)
def get_profile_url(context):
    """Returns the current URL of the profile page for the current language."""
    request = context.get("request")

    current_locale = Locale.get_active()

    profile_page = ProfilePage.objects.filter(live=True, locale=current_locale).first()

    if not profile_page:
        profile_page = ProfilePage.objects.filter(live=True).first()

    if profile_page and request:
        return profile_page.get_url(request)

    return "/"
