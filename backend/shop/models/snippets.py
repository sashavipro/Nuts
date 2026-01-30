"""shop/models/snippets.py."""

from django.db import models
from wagtail.snippets.models import register_snippet


@register_snippet
class ProductTaste(models.Model):
    """Snippet for product tastes (e.g., Sweet, Salty)."""
    name = models.CharField("Вкус", max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)


@register_snippet
class ProductPackaging(models.Model):
    """Snippet for product packaging types."""
    name = models.CharField("Упаковка", max_length=255)

    def __str__(self):
        return str(self.name)


@register_snippet
class DeliveryMethod(models.Model):
    """Snippet for available delivery methods."""
    name = models.CharField("Метод доставки", max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    is_need_address = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


@register_snippet
class PaymentMethod(models.Model):
    """Snippet for available payment methods."""
    name = models.CharField("Метод оплаты", max_length=255)

    def __str__(self):
        return str(self.name)
