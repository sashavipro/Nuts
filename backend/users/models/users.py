"""users/models/users.py."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from home.blocks import ContactsMapBlock


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('physical', 'Физическое лицо'),
        ('legal', 'Юридическое лицо'),
        ('fop', 'ФОП'),
    ]
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES,
        default='physical', verbose_name="Тип пользователя"
    )

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True, null=True)

    company_name = models.CharField("Название компании", max_length=255, blank=True)
    okpo = models.CharField("ОКПО / ЕДРПОУ", max_length=20, blank=True)

    country = models.CharField("Страна", max_length=100, blank=True)
    region = models.CharField("Область", max_length=100, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    address_line = models.CharField("Адрес", max_length=255, blank=True)

    manager_name = models.CharField(
        "Имя менеджера",
        max_length=100, blank=True,
        default="Олег"
    )
    manager_phone = models.CharField(
        "Телефон менеджера",
        max_length=20, blank=True,
        default="+38 067 777 14 12"
    )

    def __str__(self):
        return self.email or self.username


class RegistrationPage(Page):
    """Функциональная страница регистрации (без контента)"""
    max_count = 1

    def serve(self, request, *args, **kwargs):
        return render(request, 'users/registration_page.html', {'page': self})


class LoginPage(Page):
    """Страница входа"""
    max_count = 1

    intro = models.TextField("Текст инструкции", blank=True)
    footer_blocks = StreamField(
        [('contacts', ContactsMapBlock())],
        use_json_field=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('footer_blocks'),
    ]

    def serve(self, request, *args, **kwargs):
        return render(request, 'users/login_page.html', {'page': self})


class PasswordRecoveryPage(Page):
    intro = models.TextField(
        "Текст инструкции",
        default="Введите Email Вашего аккаунта..."
    )

    footer_blocks = StreamField(
        [('contacts', ContactsMapBlock())],
        use_json_field=True, blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('footer_blocks')
    ]
