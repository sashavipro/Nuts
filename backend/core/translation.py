"""core/translation.py."""

from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    """
    Translation options for the SiteSettings model.

    Specifies which fields of the SiteSettings model should be translated
    using django-modeltranslation.
    """

    fields = (
        "discount_text",
        "logo_text",
        "call_text",
        "developer_text",
        "copyright_text",
    )
