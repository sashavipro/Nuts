"""core/templatetags/navigation_tags.py."""

import logging
from django import template
from wagtail.models import Page, Site, Locale
from django.templatetags.static import static
from django_vite.templatetags.django_vite import vite_asset_url
from django_vite.core.exceptions import DjangoViteAssetNotFoundError

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

    if not site or not site.root_page:
        logger.warning("Site or root_page not found for request in get_site_root.")
        return None

    root_page = site.root_page
    current_locale = Locale.get_active()

    if getattr(root_page, "locale", None) == current_locale:
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


def _get_localized_page_url(model_class, request):
    """A universal assistant for searching for a page URL based on language."""
    current_locale = Locale.get_active()
    page = model_class.objects.filter(live=True, locale=current_locale).first()

    if not page:
        page = model_class.objects.filter(live=True).first()

    return page.get_url(request) if page and request else "/"


@register.simple_tag(takes_context=True)
def get_shop_url(context):
    """Returns the current URL of the shop page for the active language."""
    from shop.models import ShopIndexPage

    return _get_localized_page_url(ShopIndexPage, context.get("request"))


@register.simple_tag(takes_context=True)
def get_cart_url(context):
    """Returns the current URL of the shopping cart page for the active language."""
    from shop.models import CartPage

    return _get_localized_page_url(CartPage, context.get("request"))


@register.simple_tag(takes_context=True)
def get_profile_url(context):
    """Returns the current URL of the user profile page for the active language."""
    from users.models import ProfilePage

    return _get_localized_page_url(ProfilePage, context.get("request"))


@register.simple_tag(takes_context=True)
def get_checkout_url(context):
    """Returns the current URL of the checkout page for the active language."""
    from shop.models import CheckoutPage

    return _get_localized_page_url(CheckoutPage, context.get("request"))


@register.simple_tag(takes_context=True)
def safe_vite_asset(context, path):
    """
    Attempts to load the path via Vite.
    If the file is not in the manifest, it does not crash the server,
    but writes a warning to the log and returns the usual static.
    """
    try:
        return vite_asset_url(path)
    except DjangoViteAssetNotFoundError:
        logger.warning(f"Vite asset missing: {path}")
        # Если Vite не нашел файл, отдаем через стандартный static
        return static(path)
