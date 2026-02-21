"""users/views.py."""

import logging
from django.shortcuts import redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from .forms import CustomUserCreationForm, CustomPasswordResetForm

logger = logging.getLogger(__name__)


class RegisterView(CreateView):  # pylint: disable=too-many-ancestors
    """
    View to handle user registration.

    Uses CustomUserCreationForm to create a new user instance.
    Redirects to the homepage ('/') upon successful registration.
    """

    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = "/"

    def form_valid(self, form):
        """
        Handles valid form submission.

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
        """
        Handles invalid form submission.

        Logs the errors and displays an error message to the user.
        """
        logger.warning("Registration failed: %s", form.errors)
        messages.error(self.request, _("Пожалуйста, исправьте ошибки в форме."))
        return super().form_invalid(form)


class CustomPasswordResetView(auth_views.PasswordResetView):  # pylint: disable=too-many-ancestors
    """
    View for requesting a password reset.

    Uses CustomPasswordResetForm to handle asynchronous email sending.
    """

    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        logger.info(
            "Password reset requested for email: %s", form.cleaned_data["email"]
        )
        return super().form_valid(form)


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):  # pylint: disable=too-many-ancestors
    """
    View for handling the password reset confirmation.

    Users enter their new password here. Upon success, they are logged in automatically.
    """

    template_name = "users/password_reset_confirm.html"
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend="users.backends.EmailOrUsernameModelBackend")
        messages.success(self.request, _("Пароль успешно изменен! Вы авторизованы."))
        return redirect(self.success_url)
