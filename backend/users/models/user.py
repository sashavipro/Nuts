"""users/models/user.py."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with additional fields for profile and managers."""

    USER_TYPE_CHOICES = [
        ("physical", "Физическое лицо"),
        ("legal", "Юридическое лицо"),
        ("fop", "ФОП"),
    ]
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default="physical",
        verbose_name="Тип пользователя",
    )

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)

    company_name = models.CharField("Название компании", max_length=255, blank=True)
    okpo = models.CharField("ОКПО / ЕДРПОУ", max_length=20, blank=True)

    country = models.CharField("Страна", max_length=100, blank=True)
    region = models.CharField("Область", max_length=100, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    address_line = models.CharField("Адрес", max_length=255, blank=True)

    manager_name = models.CharField(
        "Имя менеджера", max_length=100, blank=True, default="Олег"
    )
    manager_phone = models.CharField(
        "Телефон менеджера", max_length=20, blank=True, default="+38 067 777 14 12"
    )

    def __str__(self):
        return self.email or self.username
