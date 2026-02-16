"""users/backends.py."""

import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpRequest

logger = logging.getLogger(__name__)


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend to allow login via Email or Username.
    """

    def authenticate(
        self, request: HttpRequest, username=None, password=None, **kwargs
    ):
        """
        Check credentials against either email or username.
        """
        user_model = get_user_model()

        if username is None:
            return None

        try:
            user = user_model.objects.get(Q(username=username) | Q(email=username))
            logger.debug("User found for login attempt: %s", username)
        except user_model.DoesNotExist:
            logger.warning("Login failed: User not found for '%s'", username)
            return None
        except user_model.MultipleObjectsReturned:
            logger.error("Login error: Multiple users found for '%s'", username)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            logger.info("User %s authenticated successfully.", user.username)
            return user

        logger.warning("Login failed: Invalid password for user '%s'", username)
        return None
