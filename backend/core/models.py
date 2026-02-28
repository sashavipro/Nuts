"""core/models.py"""

import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

logger = logging.getLogger(__name__)


class SocialMediaLink(Orderable):
    """
    Model representing an individual social media or messenger link.

    Inherits from Orderable to allow manual sorting in the Wagtail admin.
    """

    setting = ParentalKey(
        "core.SiteSettings", on_delete=models.CASCADE, related_name="social_links"
    )

    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("youtube", "YouTube"),
        ("viber", "Viber"),
        ("telegram", "Telegram"),
        ("whatsapp", "WhatsApp"),
    ]

    LINK_TYPE_CHOICES = [
        ("social", _("Социальная сеть (Вверху слева и в подвале)")),
        ("messenger", _("Мессенджер (Возле номеров телефонов)")),
    ]

    platform = models.CharField(
        _("Платформа/Иконка"), max_length=50, choices=PLATFORM_CHOICES
    )
    link_type = models.CharField(
        _("Расположение"), max_length=20, choices=LINK_TYPE_CHOICES, default="social"
    )
    url = models.URLField(_("Ссылка"))

    class Meta:
        """
        Meta options for the SocialMediaLink model.
        """

        verbose_name = _("Социальная сеть")
        verbose_name_plural = _("Социальные сети")

    def __str__(self):
        """
        Returns the string representation of the social link based on its platform.
        """
        return f"{self.platform}: {self.url}"


@register_setting
class SiteSettings(BaseSiteSetting, ClusterableModel):
    """
    Global site settings managed via Wagtail.

    Includes global header/footer content, contact information, and logo settings.
    Uses ClusterableModel to support InlinePanel for social media links.
    """

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Логотип"),
    )

    logo_text = models.CharField(_("Текст логотипа"), max_length=255, default="Nuts")
    discount_text = models.CharField(
        _("Текст скидки"), max_length=255, default=_("Скидка -10% на первый заказ")
    )

    phone_1_code = models.CharField(_("Код 1"), max_length=10, default="+38 (067)")
    phone_1_number = models.CharField(_("Номер 1"), max_length=20, default="555-55-55")
    phone_2_code = models.CharField(_("Код 2"), max_length=10, default="+38 (063)")
    phone_2_number = models.CharField(_("Номер 2"), max_length=20, default="333-33-33")
    call_text = models.CharField(
        _("Текст звонка"), max_length=100, default=_("Заказать звонок")
    )

    developer_text = models.TextField(
        _("Текст разработчика"),
        default='Разработано <a href="#" class="dev"><span>AVADA</span> MEDIA</a>',
    )
    copyright_text = models.CharField(
        _("Копирайт"), max_length=255, default=_("Copyright © 2019. Все права защищены")
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("logo"),
                FieldPanel("logo_text_ru"),
                FieldPanel("logo_text_uk"),
                FieldPanel("logo_text_en"),
                FieldPanel("discount_text_ru"),
                FieldPanel("discount_text_uk"),
                FieldPanel("discount_text_en"),
            ],
            heading=_("Шапка: Логотип и скидка"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("phone_1_code"),
                FieldPanel("phone_1_number"),
                FieldPanel("phone_2_code"),
                FieldPanel("phone_2_number"),
                FieldPanel("call_text_ru"),
                FieldPanel("call_text_uk"),
                FieldPanel("call_text_en"),
            ],
            heading=_("Шапка: Контакты"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("developer_text_ru"),
                FieldPanel("developer_text_uk"),
                FieldPanel("developer_text_en"),
                FieldPanel("copyright_text_ru"),
                FieldPanel("copyright_text_uk"),
                FieldPanel("copyright_text_en"),
            ],
            heading=_("Подвал сайта"),
        ),
        InlinePanel("social_links", label=_("Ссылки на соцсети")),
    ]

    class Meta:
        """
        Meta options for SiteSettings.
        """

        verbose_name = _("Настройки сайта")

    def save(self, *args, **kwargs):
        """
        Overrides the save method to log site setting updates.
        """
        logger.info("SiteSettings are being updated by user.")
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a generic string representation for SiteSettings.
        """
        return "Global Site Settings"
