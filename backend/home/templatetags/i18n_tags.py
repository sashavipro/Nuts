"""home/templatetags/i18n_tags.py."""

import logging
from django import template
from wagtail.models import Page, Site, Locale

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def get_translated_url(context, lang_code):
    """
    Returns the URL of the current page translated into the target language (lang_code).
    If no translation exists, returns the URL of the homepage for that language.
    """
    page = context.get("page")
    request = context.get("request")

    locale = Locale.objects.filter(language_code=lang_code).first()

    if not locale:
        logger.error("Locale with language code '%s' does not exist.", lang_code)
        return f"/{lang_code}/"

    if isinstance(page, Page):
        translated_page = page.get_translation_or_none(locale)
        if translated_page and translated_page.live:
            return translated_page.url

    if request:
        site = Site.find_for_request(request)
        if site:
            root = site.root_page.get_translation_or_none(locale)
            if root and root.live:
                return root.url

    return f"/{lang_code}/"
