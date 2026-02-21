"""shop/models/snippets.py."""

import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.models import register_snippet

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods


@register_snippet
class ProductTaste(models.Model):
    """
    Snippet for managing Product Tastes via Wagtail.
    """

    name = models.CharField(_("Вкус"), max_length=255)

    class Meta:
        """
        Meta options for ProductTaste.
        """

        verbose_name = _("Вкус")
        verbose_name_plural = _("Справочник: Вкусы")

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

    name = models.CharField(
        _("Вес"), max_length=50, help_text=_("Например: 40г, 100г, 200г")
    )
    value = models.IntegerField(_("Значение в граммах"), help_text=_("Для сортировки"))

    class Meta:
        """
        Meta options for ProductWeight.
        """

        verbose_name = _("Вес")
        verbose_name_plural = _("Справочник: Вес")
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

    name = models.CharField(_("Упаковка"), max_length=255)

    class Meta:
        """
        Meta options for ProductPackaging.
        """

        verbose_name = _("Упаковка")
        verbose_name_plural = _("Справочник: Упаковки")

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
