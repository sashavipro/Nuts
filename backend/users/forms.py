"""users/forms.py."""

import logging
from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.template import loader
from django.utils.translation import gettext_lazy as _
from cities_light.models import Region
from .models import CustomUser
from .tasks import send_reset_email_task

logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):  # pylint: disable=too-many-ancestors
    """
    Form for registering a new CustomUser.

    Handles dynamic loading of regions based on the selected country
    and conditional validation for user types (Physical, Legal, FOP).
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options for CustomUserCreationForm."""

        model = CustomUser

        # pylint: disable=duplicate-code
        fields = (
            "user_type",
            "is_fop",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone",
            "avatar",
            "company_name",
            "okpo",
            "country",
            "region",
            "city",
            "address_line",
            "zip_code",
        )
        widgets = {
            "country": forms.Select(
                attrs={"class": "form-control", "id": "id_country"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, sets CSS classes, and handles dynamic region loading.
        """
        super().__init__(*args, **kwargs)

        logger.debug("Initializing CustomUserCreationForm")

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        self.fields["country"].empty_label = _("Выберите страну")
        self.fields["country"].widget.attrs.update({"id": "id_country"})

        self.fields["region"].queryset = Region.objects.none()
        self.fields["region"].widget.attrs.update(
            {"id": "id_region", "disabled": "true"}
        )

        if "country" in self.data:
            try:
                country_id = int(self.data.get("country"))
                self.fields["region"].queryset = Region.objects.filter(
                    country_id=country_id
                ).order_by("name")
                self.fields["region"].widget.attrs.pop("disabled", None)
                logger.debug(
                    "Loaded regions for country_id=%s from POST data", country_id
                )
            except (ValueError, TypeError) as e:
                logger.warning("Error parsing country_id from data: %s", e)

        elif self.instance.pk and self.instance.country:
            self.fields["region"].queryset = self.instance.country.region_set.order_by(
                "name"
            )
            logger.debug(
                "Loaded regions for country=%s from instance", self.instance.country
            )

        self.fields["company_name"].required = False
        self.fields["okpo"].required = False
        self.fields["city"].widget.attrs["placeholder"] = _("Город")
        self.fields["company_name"].widget.attrs["placeholder"] = _("Название компании")
        self.fields["okpo"].widget.attrs["placeholder"] = _("ОКПО / ЕДРПОУ")
        self.fields["zip_code"].widget.attrs["placeholder"] = _("Индекс")
        self.fields["address_line"].widget.attrs["placeholder"] = _(
            "Адрес (улица, дом, кв.)"
        )
        self.fields["first_name"].widget.attrs["placeholder"] = _("Имя*")
        self.fields["last_name"].widget.attrs["placeholder"] = _("Фамилия*")
        self.fields["middle_name"].widget.attrs["placeholder"] = _("Отчество")
        self.fields["email"].widget.attrs["placeholder"] = _("Email*")
        self.fields["phone"].widget.attrs["placeholder"] = _("Телефон*")

    def clean(self):
        """
        Validates the form data based on the selected user type.

        Cleans up irrelevant fields (e.g., company info for physical users)
        and enforces requirements for legal entities.
        """
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        logger.debug("Cleaning form data for user_type: %s", user_type)

        if user_type == "physical":
            cleaned_data["company_name"] = ""
            cleaned_data["okpo"] = ""
            cleaned_data["is_fop"] = False

        elif user_type == "fop":
            cleaned_data["is_fop"] = True
            cleaned_data["company_name"] = ""
            cleaned_data["okpo"] = ""

        elif user_type == "legal":
            cleaned_data["is_fop"] = False
            if not cleaned_data.get("company_name"):
                self.add_error(
                    "company_name",
                    _("Название компании обязательно для юридических лиц."),
                )
                logger.warning(
                    "Validation error: Missing company_name for Legal entity"
                )
            if not cleaned_data.get("okpo"):
                self.add_error("okpo", _("Код ЕДРПОУ обязателен для юридических лиц."))
                logger.warning("Validation error: Missing okpo for Legal entity")

        return cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
    """
    Custom password reset form that delegates email sending to Celery.
    """

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):  # pylint: disable=too-many-arguments, too-many-positional-arguments
        """
        Overrides the default synchronous send_mail method.

        Renders templates to strings and schedules a Celery task.
        """
        logger.debug("Preparing async password reset for: %s", to_email)

        subject = loader.render_to_string(subject_template_name, context)
        subject = "".join(subject.splitlines())

        body = loader.render_to_string(email_template_name, context)

        html_email = None
        if html_email_template_name:
            html_email = loader.render_to_string(html_email_template_name, context)

        send_reset_email_task.delay(
            subject=subject,
            body=body,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_email,
        )

        logger.info("Password reset task queued for %s", to_email)
