"""users/models/user.py."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from cities_light.models import Country, Region


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Includes additional fields for profile management, location (country/region),
    and separation between physical and legal entities.
    """

    class UserType(models.TextChoices):
        """Enumeration for user types."""

        PHYSICAL = "physical", "Физическое лицо"
        LEGAL = "legal", "Юридическое лицо"
        FOP = "fop", "ФОП"

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.PHYSICAL,
        verbose_name="Тип пользователя",
    )
    is_fop = models.BooleanField("Являюсь ФОП", default=False)

    middle_name = models.CharField("Отчество", max_length=150, blank=True)

    phone_regex = RegexValidator(
        regex=r"^\+\d{1,4}\s?\d{1,4}\s?\d{1,4}\s?\d{0,4}\s?\d{0,4}$",
        message="Номер телефона должен быть в формате: '+999 99 999 99 99'",
    )
    phone = models.CharField(
        "Телефон", validators=[phone_regex], max_length=30, blank=True
    )

    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)

    company_name = models.CharField("Название компании", max_length=255, blank=True)
    okpo = models.CharField("ОКПО / ЕДРПОУ", max_length=20, blank=True)

    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Страна"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Область/Регион",
    )
    city = models.CharField("Город", max_length=100, blank=True)
    address_line = models.CharField("Адрес", max_length=255, blank=True)
    zip_code = models.CharField("Почтовый индекс", max_length=20, blank=True)

    manager_name = models.CharField("Имя менеджера", max_length=100, blank=True)
    manager_phone = models.CharField("Телефон менеджера", max_length=20, blank=True)

    class Meta:
        """Meta options for the CustomUser model."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

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
        return self.phone if self.phone else "Не указан"
