"""mysite/settings/production.py."""

import contextlib

from .base import *  # noqa: F403

SECRET_KEY = env("SECRET_KEY")  # noqa: F405
DEBUG = env.bool("DEBUG", default=False)  # noqa: F405
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])  # noqa: F405
DJANGO_VITE_DEV_MODE = env.bool("DJANGO_VITE_DEV_MODE", default=False)  # noqa: F405

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])  # noqa: F405

# На локальном тесте по http:// ставим False, на боевом сервере — True
USE_HTTPS = env.bool("USE_HTTPS", default=True)  # noqa: F405
SESSION_COOKIE_SECURE = USE_HTTPS
CSRF_COOKIE_SECURE = USE_HTTPS

# Fix: Shortened long URL/comment line
# See: https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/
STORAGES["staticfiles"]["BACKEND"] = "mysite.storage.TolerantManifestStorage"  # noqa: F405

# Fix: Replaced try-except-pass with contextlib.suppress
with contextlib.suppress(ImportError):
    from .local import *  # noqa: F403
