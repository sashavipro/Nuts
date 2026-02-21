"""shop/admin.py"""

import logging

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, StackedInline
from unfold.decorators import action, display

from .models import Product, ProductGalleryImage

logger = logging.getLogger(__name__)


class ProductGalleryImageInline(StackedInline):
    """
    Inline admin interface for managing product gallery images within the Product admin.
    """

    model = ProductGalleryImage
    extra = 1
    fields = ["image"]
    ordering_field = "sort_order"

    verbose_name = _("Изображение")
    verbose_name_plural = _("Галерея изображений")


@admin.register(Product)
class ProductAdmin(ModelAdmin, TabbedTranslationAdmin):
    """
    Admin interface for the Product model using Unfold and ModelTranslation.
    """

    list_display = [
        "title",
        "sku",
        "price",
        "gallery_count",
        "is_new",
        "is_sale",
        "live",
        "created_at",
    ]

    search_fields = ["title", "sku"]
    list_filter = ["live", "is_new", "is_sale", "tastes", "weight_option", "packaging"]
    list_editable = ["price", "live"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductGalleryImageInline]
    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": (
                    "title",
                    "slug",
                    "sku",
                    "price",
                    "old_price",
                    "weight_option",
                    "live",
                ),
            },
        ),
        (
            _("Маркетинг"),
            {
                "fields": ("is_new", "is_sale"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Характеристики"),
            {
                "fields": ("composition", "energy_value", "shelf_life"),
            },
        ),
        (
            _("Связи"),
            {
                "fields": ("tastes", "packaging"),
            },
        ),
    )

    @display(description=_("Фото"))
    def gallery_count(self, obj):
        """
        Displays the count of images in the product gallery with visual formatting.
        """
        count = obj.gallery_images.count()
        if count > 0:
            return format_html('<span style="color: green;">✓ {} фото</span>', count)
        return format_html('<span style="color: red;">{}</span>', _("✗ Нет фото"))

    @action(description=_("Опубликовать выбранные товары"))
    def make_published(self, request, queryset):
        """
        Admin action to bulk publish selected products (set live=True).
        """
        updated_count = queryset.update(live=True)
        logger.info(
            "User %s published %d products via admin action.",
            request.user,
            updated_count,
        )

    actions = [make_published]
