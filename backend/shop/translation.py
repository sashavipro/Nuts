"""shop/translation.py"""

from modeltranslation.translator import register, TranslationOptions
from .models import Product


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    """
    Configuration for translating specific fields of
    the Product model using django-modeltranslation.
    """

    fields = (
        "title",
        "slug",
        "composition",
        "energy_value",
        "shelf_life",
    )
