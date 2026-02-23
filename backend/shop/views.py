"""shop/views.py"""

import logging
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models.ecommerce import Order, OrderSuccessPage, PaymentTransaction

# pylint: disable=no-member

logger = logging.getLogger(__name__)


def mock_payment(request, order_number):
    """
    Mock payment gateway page (simulating LiqPay/WayForPay/etc.).

    Processes a dummy payment, securely updates the order status,
    creates a transaction record atomically, and redirects to success.
    """
    order = get_object_or_404(Order, order_number=order_number)

    if request.method == "POST":
        try:
            with transaction.atomic():
                order.status = Order.Status.PROCESSING
                order.save()

                if request.user.is_authenticated:
                    trans_obj = PaymentTransaction.objects.create(
                        user=request.user,
                        amount=order.total_amount,
                        description=f"Payment for order {order.order_number}",
                    )
                    logger.info(
                        "PaymentTransaction ID %s created for order %s.",
                        trans_obj.id,
                        order.order_number,
                    )

            logger.info(
                "Order %s status updated to PROCESSING after mock payment.",
                order.order_number,
            )

            success_page = OrderSuccessPage.objects.live().first()
            if success_page:
                logger.debug(
                    "Redirecting order %s to OrderSuccessPage.", order.order_number
                )
                return redirect(success_page.url)

            logger.warning("OrderSuccessPage not found. Redirecting to home ('/').")
            return redirect("/")

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error(
                "Error processing mock payment for order %s: %s", order.order_number, e
            )

    return render(request, "shop/payment.html", {"order": order})
