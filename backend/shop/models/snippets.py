"""shop/models/snippets.py."""

import logging
from django.db import models
from wagtail.snippets.models import register_snippet

logger = logging.getLogger(__name__)


@register_snippet
class ProductTaste(models.Model):
    """
    Snippet for managing Product Tastes via Wagtail.
    """

    name = models.CharField("Вкус", max_length=255)

    class Meta:
        """
        Meta options for ProductTaste.
        """

        verbose_name = "Вкус"
        verbose_name_plural = "Справочник: Вкусы"

    def __str__(self):
        """
        String representation of the ProductTaste.
        """
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        Saves the ProductTaste instance and logs the action.
        """
        logger.info("Saving ProductTaste: %s", self.name)
        super().save(*args, **kwargs)


@register_snippet
class ProductWeight(models.Model):
    """
    Snippet for managing Product Weights via Wagtail.
    Includes a value field for sorting purposes.
    """

    name = models.CharField("Вес", max_length=50, help_text="Например: 40г, 100г, 200г")
    value = models.IntegerField("Значение в граммах", help_text="Для сортировки")

    class Meta:
        """
        Meta options for ProductWeight.
        """

        verbose_name = "Вес"
        verbose_name_plural = "Справочник: Вес"
        ordering = ["value"]

    def __str__(self):
        """
        String representation of the ProductWeight.
        """
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        Saves the ProductWeight instance and logs the action.
        """
        logger.info("Saving ProductWeight: %s", self.name)
        super().save(*args, **kwargs)


@register_snippet
class ProductPackaging(models.Model):
    """
    Snippet for managing Product Packaging types via Wagtail.
    """

    name = models.CharField("Упаковка", max_length=255)

    class Meta:
        """
        Meta options for ProductPackaging.
        """

        verbose_name = "Упаковка"
        verbose_name_plural = "Справочник: Упаковки"

    def __str__(self):
        """
        String representation of the ProductPackaging.
        """
        return str(self.name)

    def save(self, *args, **kwargs):
        """
        Saves the ProductPackaging instance and logs the action.
        """
        logger.info("Saving ProductPackaging: %s", self.name)
        super().save(*args, **kwargs)
