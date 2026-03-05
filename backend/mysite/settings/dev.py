"""mysite/settings/dev.py."""

import contextlib

from .base import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)  # noqa: F405

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="django-insecure-dev-key")  # noqa: F405

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])  # noqa: F405

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Fix: Replaced try-except-pass with contextlib.suppress
with contextlib.suppress(ImportError):
    from .local import *  # noqa: F403
