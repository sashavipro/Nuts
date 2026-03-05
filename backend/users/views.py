"""users/views.py."""

import logging

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView

from .forms import CustomPasswordResetForm, CustomUserCreationForm
from .models import RegistrationPage, TermsOfUsePage

logger = logging.getLogger(__name__)


class RegisterView(CreateView):  # pylint: disable=too-many-ancestors
    """View to handle user registration.

    Uses CustomUserCreationForm to create a new user instance.
    Redirects to the homepage ('/') upon successful registration.
    """

    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        """Injects the TermsOfUsePage URL into the template context."""
        context = super().get_context_data(**kwargs)
        reg_page = RegistrationPage.objects.live().first()
        if reg_page:
            context["terms_page"] = (
                TermsOfUsePage.objects.descendant_of(reg_page).live().first()
            )
        return context

    def form_valid(self, form):
        """Handle valid form submission.

        Saves the user, logs them in, and displays a success message.
        """
        user = form.save()
        login(self.request, user, backend="users.backends.EmailOrUsernameModelBackend")

        logger.info("New user registered and logged in: %s", user.username)
        messages.success(
            self.request, _("Добро пожаловать, {name}!").format(name=user.first_name)
        )
        return redirect(self.success_url)

    def form_invalid(self, form):
        """Handle invalid form submission.

        Logs the errors and displays an error message to the user.
        """
        logger.warning("Registration failed: %s", form.errors)
        messages.error(self.request, _("Пожалуйста, исправьте ошибки в форме."))
        return super().form_invalid(form)


class CustomPasswordResetView(auth_views.PasswordResetView):  # pylint: disable=too-many-ancestors
    """View for requesting a password reset.

    Uses CustomPasswordResetForm to handle asynchronous email sending.
    """

    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        """Handle valid form submission by logging the email request."""
        logger.info(
            "Password reset requested for email: %s", form.cleaned_data["email"]
        )
        return super().form_valid(form)


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):  # pylint: disable=too-many-ancestors
    """View for handling the password reset confirmation.

    Users enter their new password here. Upon success, they are logged in automatically.
    """

    template_name = "users/password_reset_confirm.html"
    success_url = "/"

    def form_valid(self, form):
        """Handle valid form submission, save new password, and login user."""
        user = form.save()
        login(self.request, user, backend="users.backends.EmailOrUsernameModelBackend")
        messages.success(self.request, _("Пароль успешно изменен! Вы авторизованы."))
        return redirect(self.success_url)
