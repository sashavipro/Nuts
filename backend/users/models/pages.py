"""users/models/pages.py."""

from contacts.blocks import ContactImportBlock  # Импортируем блок контактов
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class RegistrationPage(Page):
    """Wagtail model for the Registration page.

    Acts as a parent container for the Terms of Use page.
    """

    max_count = 1
    subpage_types = ["users.TermsOfUsePage"]

    def serve(self, request, *args, **kwargs):
        """Redirect from an empty Wagtail page to the actual registration form."""
        return redirect("register")


class TermsOfUsePage(Page):
    """Wagtail model for the Terms of Use (Пользовательское соглашение) page.

    Restricted to be a child of the RegistrationPage.
    """

    body = RichTextField(verbose_name=_("Текст соглашения"))

    footer_blocks = StreamField(
        [
            ("contacts_section", ContactImportBlock(label=_("Блок контактов"))),
        ],
        use_json_field=True,
        blank=True,
        verbose_name=_("Подвал (контакты)"),
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("body"),
        FieldPanel("footer_blocks"),
    ]

    parent_page_types = ["users.RegistrationPage"]
    subpage_types = []
    template = "users/terms_of_use_page.html"

    class Meta:
        """Meta options for TermsOfUsePage."""

        verbose_name = _("Пользовательское соглашение")
