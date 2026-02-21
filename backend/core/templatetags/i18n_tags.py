"""core/templatetags/i18n_tags.py."""

import logging
from django import template
from django.urls import translate_url, resolve, Resolver404
from wagtail.models import Page, Site, Locale

logger = logging.getLogger(__name__)
register = template.Library()


def _get_wagtail_translated_url(request, page, lang_code):
    """
    Helper function to get the translated URL for a Wagtail page.
    Falls back to the translated root page if the current page translation is missing.
    """
    locale = Locale.objects.filter(language_code=lang_code).first()
    if not locale:
        return f"/{lang_code}/"

    if isinstance(page, Page):
        translated_page = page.get_translation_or_none(locale)
        if translated_page and translated_page.live:
            return translated_page.get_url(request)

    site = Site.find_for_request(request)
    if site and site.root_page:
        translated_root = site.root_page.get_translation_or_none(locale)
        if translated_root and translated_root.live:
            return translated_root.get_url(request)

    return f"/{lang_code}/"


@register.simple_tag(takes_context=True)
def get_translated_url(context, lang_code):
    """
    Retrieves the translated URL for the current page or path.
    Handles both Wagtail pages and standard Django views.
    """
    request = context.get("request")
    if not request:
        return f"/{lang_code}/"

    page = context.get("page")

    is_wagtail_page = isinstance(page, Page)
    if not is_wagtail_page:
        try:
            if resolve(request.path).url_name == "wagtail_serve":
                is_wagtail_page = True
        except Resolver404:
            pass

    if is_wagtail_page:
        return _get_wagtail_translated_url(request, page, lang_code)

    try:
        url = translate_url(request.path, lang_code)
        if url:
            return url
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error translating django url: %s", e)

    return f"/{lang_code}/"
