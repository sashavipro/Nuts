"""shop/forms.py"""

import logging
from django import forms
from django.utils.translation import gettext_lazy as _
from .models.ecommerce import Order

logger = logging.getLogger(__name__)

# pylint: disable=too-few-public-methods, cyclic-import


class CheckoutForm(forms.ModelForm):
    """
    Checkout form handling order creation.

    Dynamically enforces required fields based on the selected delivery method.
    """

    class Meta:
        """Meta options mapping the form to the Order model."""

        model = Order
        fields = [
            "first_name",
            "phone",
            "email",
            "city",
            "address_line",
            "company_name",
            "okpo",
            "delivery_method",
            "payment_method",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": _("Компания")}),
            "first_name": forms.TextInput(attrs={"placeholder": _("Контактное лицо*")}),
            "email": forms.EmailInput(attrs={"placeholder": "Email*"}),
            "phone": forms.TextInput(attrs={"placeholder": _("Телефон*")}),
            "city": forms.TextInput(attrs={"placeholder": _("Город*")}),
            "address_line": forms.TextInput(
                attrs={"placeholder": _("Улица, дом, квартира*")}
            ),
            "okpo": forms.TextInput(attrs={"placeholder": _("ОКПО / ЕДРПОУ")}),
        }

    def clean(self):
        """
        Validates the entire form payload.

        Ensures that shipping addresses are provided correctly depending
        on whether the user selected Nova Poshta, Courier, or Pickup.
        """
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get("delivery_method")

        city = cleaned_data.get("city")
        address_line = cleaned_data.get("address_line")

        if delivery_method == Order.Delivery.NOVA_POSHTA:
            if not city:
                self.add_error("city", _("Укажите город для доставки Новой Почтой."))
                logger.debug("Checkout validation error: Missing city for Nova Poshta.")
            if not address_line:
                self.add_error(
                    "address_line", _("Укажите номер отделения Новой Почты.")
                )
                logger.debug(
                    "Checkout validation error: Missing branch for Nova Poshta."
                )

        elif delivery_method == Order.Delivery.COURIER:
            if not city:
                self.add_error("city", _("Укажите город для курьерской доставки."))
            if not address_line:
                self.add_error("address_line", _("Укажите улицу, дом и квартиру."))

        elif delivery_method == Order.Delivery.PICKUP:
            # Clear addressing data if pickup is selected to keep DB clean
            cleaned_data["city"] = ""
            cleaned_data["address_line"] = ""

        return cleaned_data
