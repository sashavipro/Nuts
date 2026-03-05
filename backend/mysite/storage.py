"""mysite/storage.py."""

import logging

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

logger = logging.getLogger(__name__)


class TolerantManifestStorage(ManifestStaticFilesStorage):
    """Custom static file storage, resistant to missing dependencies."""

    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        """Generate a file name with a unique hash to invalidate the browser cache."""
        try:
            return super().hashed_name(name, content, filename)
        except ValueError as e:
            # Fix: Use %s interpolation instead of f-string for logging
            logger.warning("Missing file skipped during static compilation: %s", e)
            return name
