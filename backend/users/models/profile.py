"""users/models/profile.py."""

import logging

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import models, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Page

from contacts.blocks import ContactImportBlock
from shop.models.ecommerce import Order, PaymentTransaction
from users.forms import UserAddressForm, UserContactInfoForm

# pylint: disable=no-member, disable=duplicate-code

logger = logging.getLogger(__name__)


class ProfilePage(RoutablePageMixin, Page):  # pylint: disable=too-many-ancestors
    """
    User profile page managing dashboard, orders, and transactions.

    Provides routable endpoints for viewing order history, managing
    contact info, updating addresses, and changing passwords securely.
    """

    manager_title = models.CharField(
        max_length=255,
        default=_("Ваш личный менеджер Олег"),
        verbose_name=_("Текст 'Личный менеджер'"),
    )
    manager_phone = models.CharField(
        max_length=50, default="+38 067 777 14 12", verbose_name=_("Телефон менеджера")
    )

    footer_blocks = StreamField(
        [
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name=_("Блок контактов"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("manager_title"),
        FieldPanel("manager_phone"),
        FieldPanel("footer_blocks"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]

    def _check_authentication(self, request):
        """
        Redirects to the login page if the user is not authenticated.
        """
        if not request.user.is_authenticated:
            logger.debug(
                "Unauthenticated access attempt to ProfilePage endpoint: %s",
                request.path,
            )
            return redirect(f"{reverse('login')}?next={request.path}")
        return None

    @route(r"^$")
    def dashboard(self, request):
        """
        Root profile route. Redirects to the orders history by default.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect
        return redirect(self.url + "orders/")

    @route(r"^orders/$")
    def orders(self, request):
        """
        Renders the order history view for the authenticated user.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        user_orders = Order.objects.filter(user=request.user)
        logger.debug("Rendering orders history for user ID: %s", request.user.id)

        return render(
            request, "users/profile_orders.html", {"page": self, "orders": user_orders}
        )

    @route(r"^transactions/$")
    def transactions(self, request):
        """
        Renders the transaction history view for the authenticated user.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        user_transactions = PaymentTransaction.objects.filter(
            user=request.user
        ).order_by("-created_at")

        logger.debug("Rendering transactions history for user ID: %s", request.user.id)

        return render(
            request,
            "users/profile_transactions.html",
            {"page": self, "transactions": user_transactions},
        )

    @route(r"^order/(?P<order_id>\d+)/$")
    def order_detail_modal(self, request, order_id):
        """
        Returns the HTML snippet of a modal window with specific order details.
        Protects against viewing other users' orders.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        order = get_object_or_404(Order, id=order_id, user=request.user)

        return render(request, "users/includes/order_modal.html", {"order": order})

    @route(r"^transaction/(?P<tr_id>\d+)/$")
    def transaction_detail_modal(self, request, tr_id):
        """
        Returns the HTML snippet of the modal window with transaction details.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        transaction_obj = get_object_or_404(
            PaymentTransaction, id=tr_id, user=request.user
        )

        return render(
            request,
            "users/includes/transaction_modal.html",
            {"transaction": transaction_obj},
        )

    @route(r"^address/$")
    def address(self, request):
        """
        Renders and processes the user address and billing details editing form.

        Handles POST requests to update user data within an atomic transaction
        to ensure database consistency.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        if request.method == "POST":
            form = UserAddressForm(request.POST, instance=request.user)
            if form.is_valid():
                with transaction.atomic():
                    form.save()
                logger.info(
                    "User '%s' (ID: %s) successfully updated their address.",
                    request.user.username,
                    request.user.id,
                )
                messages.success(request, _("Данные успешно сохранены!"))
                return redirect(request.path)

            logger.warning(
                "User '%s' failed to update address. Form errors: %s",
                request.user.username,
                form.errors,
            )
        else:
            form = UserAddressForm(instance=request.user)

        return render(
            request, "users/profile_address.html", {"page": self, "form": form}
        )

    @route(r"^contact-info/$")
    def contact_info(self, request):
        """
        Renders and processes the contact information and avatar editing page.

        Utilizes an atomic transaction to safely commit the file uploads and
        database changes.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        if request.method == "POST":
            form = UserContactInfoForm(
                request.POST, request.FILES, instance=request.user
            )
            if form.is_valid():
                with transaction.atomic():
                    form.save()
                logger.info(
                    "User '%s' (ID: %s) successfully updated contact information.",
                    request.user.username,
                    request.user.id,
                )
                messages.success(request, _("Контактная информация успешно сохранена!"))
                return redirect(request.path)

            logger.warning(
                "User '%s' failed to update contact info. Form errors: %s",
                request.user.username,
                form.errors,
            )
        else:
            form = UserContactInfoForm(instance=request.user)

        return render(
            request, "users/profile_contact_info.html", {"page": self, "form": form}
        )

    @route(r"^password/$")
    def password(self, request):
        """
        Renders and processes the secure password change form.

        Wraps the password update and session authentication hash update
        within an atomic transaction to ensure the user is not unexpectedly logged out.
        """
        auth_redirect = self._check_authentication(request)
        if auth_redirect:
            return auth_redirect

        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                with transaction.atomic():
                    user = form.save()
                    update_session_auth_hash(request, user)

                logger.info(
                    "User '%s' (ID: %s) successfully changed their password.",
                    user.username,
                    user.id,
                )
                messages.success(request, _("Ваш пароль успешно изменен!"))
                return redirect(request.path)

            logger.warning(
                "User '%s' failed to change password. Form errors: %s",
                request.user.username,
                form.errors,
            )
            messages.error(request, _("Пожалуйста, исправьте ошибки ниже."))
        else:
            form = PasswordChangeForm(request.user)

        return render(
            request, "users/profile_password.html", {"page": self, "form": form}
        )
