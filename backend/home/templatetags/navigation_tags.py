"""home/templatetags/navigation_tags.py."""

import logging
from django import template
from wagtail.models import Page, Site, Locale

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
