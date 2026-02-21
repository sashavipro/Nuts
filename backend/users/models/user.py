"""users/models/user.py."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, Region


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Includes additional fields for profile management, location (country/region),
    and separation between physical and legal entities.
    """

    class UserType(models.TextChoices):
        """Enumeration for user types."""

        PHYSICAL = "physical", _("Физическое лицо")
        LEGAL = "legal", _("Юридическое лицо")
        FOP = "fop", _("ФОП")

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.PHYSICAL,
        verbose_name=_("Тип пользователя"),
    )
    is_fop = models.BooleanField(_("Являюсь ФОП"), default=False)

    middle_name = models.CharField(_("Отчество"), max_length=150, blank=True)

    phone_regex = RegexValidator(
        regex=r"^\+\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{0,4}\s?\d{0,4}$",
        message=_("Номер телефона должен быть в формате: '+999 99 999 99 99'"),
    )
    phone = models.CharField(
        _("Телефон"), validators=[phone_regex], max_length=30, blank=True
    )

    avatar = models.ImageField(_("Аватар"), upload_to="avatars/", blank=True, null=True)

    company_name = models.CharField(_("Название компании"), max_length=255, blank=True)
    okpo = models.CharField(_("ОКПО / ЕДРПОУ"), max_length=20, blank=True)

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Страна"),
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Область/Регион"),
    )
    city = models.CharField(_("Город"), max_length=100, blank=True)
    address_line = models.CharField(_("Адрес"), max_length=255, blank=True)
    zip_code = models.CharField(_("Почтовый индекс"), max_length=20, blank=True)

    manager_name = models.CharField(_("Имя менеджера"), max_length=100, blank=True)
    manager_phone = models.CharField(_("Телефон менеджера"), max_length=20, blank=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options for the CustomUser model."""

        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        """
        Returns the string representation of the user.
        Usually the email or username.
        """
        return self.email or self.username

    def get_full_name(self):
        """
        Returns the full name including the middle name.
        """
        parts = [self.first_name, self.middle_name, self.last_name]
        full_name = " ".join(filter(None, parts))
        return full_name

    def get_display_phone(self):
        """
        Returns the formatted phone number or a default message.
        """
        return self.phone if self.phone else _("Не указан")
