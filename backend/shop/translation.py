"""shop/translation.py."""

from modeltranslation.translator import TranslationOptions, register

from .models import Product, ProductPackaging, ProductTaste, ProductWeight


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    """Configuration for translating specific fields of the Product model.

    Uses django-modeltranslation.
    """

    fields = (
        "title",
        "slug",
        "composition",
        "energy_value",
        "shelf_life",
    )


@register(ProductWeight)
class ProductWeightTranslationOptions(TranslationOptions):
    """Translation configuration for weight labels (e.g., 'Weight' vs 'Вес')."""

    fields = ("name",)


@register(ProductPackaging)
class ProductPackagingTranslationOptions(TranslationOptions):
    """Translation configuration for packaging type names."""

    fields = ("name",)


@register(ProductTaste)
class ProductTasteTranslationOptions(TranslationOptions):
    """Translation configuration for product flavor/taste names."""

    fields = ("name",)
