"""users/tasks.py."""

import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_reset_email_task(
    subject: str,
    body: str,
    from_email: str,
    recipient_list: list,
    html_message: str = None,
):
    """
    Async task to send password reset emails via Celery.
    """
    logger.info("Starting email task for recipients: %s", recipient_list)

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info("Email successfully sent to %s", recipient_list)
    except Exception as e:
        logger.error("Failed to send email to %s. Error: %s", recipient_list, e)
        raise e
