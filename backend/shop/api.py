"""shop/api.py"""

import json
import logging
from ninja import Router, Form
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from .models.ecommerce import get_or_create_cart, CartItem
from .models.products import Product

# pylint: disable=no-member

logger = logging.getLogger(__name__)
router = Router()


def get_cart_update_response(request, cart):
    """
    Helper function to return a single HttpResponse containing multiple OOB (Out-Of-Band)
    swaps. This seamlessly updates the mini-cart, header counter, checkout table,
    and totals without triggering multiple GET requests.
    """
    total_items = sum(item.quantity for item in cart.items.all())
    total_price = cart.get_total_price()

    html = render_to_string(
        "shop/includes/mini_cart.html", {"cart": cart}, request=request
    )

    counter_html = (
        f"<span id='cart-counter' class='quantity' "
        f"hx-swap-oob='true'>{total_items}</span>"
    )

    cart_table_html = render_to_string(
        "shop/includes/cart_table.html", {"cart": cart}, request=request
    )
    table_oob = (
        f"<div id='checkout-cart-table' hx-swap-oob='true'>{cart_table_html}</div>"
    )

    top_total_oob = (
        f'<div id="checkout-top-total" class="text-right mb-5" '
        f'style="font-size: 18px; font-weight: 700;" hx-swap-oob="true">'
        f'{_("Всего")} <span style="font-size: 20px; color: #3d8063;">'
        f"{total_price}</span> {_('грн.')}</div>"
    )

    bottom_total_oob = (
        f'<span id="checkout-bottom-total" style="font-size: 18px; '
        f'font-weight: 700;" hx-swap-oob="true">{_("Всего")} '
        f'<span style="font-size: 24px; color: #3d8063;">{total_price}</span> '
        f"{_('грн.')}</span>"
    )

    response = HttpResponse(
        html + counter_html + table_oob + top_total_oob + bottom_total_oob
    )

    triggers = {"cartUpdated": ""}
    if total_items == 0:
        triggers["cartEmpty"] = ""

    response["HX-Trigger"] = json.dumps(triggers)
    return response


@router.get("/cart/count/")
def get_cart_count(request):
    """Returns only the HTML snippet for the cart items count badge in the header."""
    cart = get_or_create_cart(request)
    total_items = sum(item.quantity for item in cart.items.all())
    return HttpResponse(
        f"<span id='cart-counter' class='quantity'>{total_items}</span>"
    )


@router.get("/cart/mini/")
def get_mini_cart(request):
    """Returns the rendered HTML template for the mini-cart dropdown."""
    cart = get_or_create_cart(request)
    html = render_to_string(
        "shop/includes/mini_cart.html", {"cart": cart}, request=request
    )
    return HttpResponse(html)


@router.post("/cart/add/{product_id}/")
def add_to_cart(request, product_id: int, quantity: int = Form(1)):
    """
    API endpoint to add a product to the cart via HTMX.
    Uses atomic transaction to ensure safe data insertion.
    """
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id, live=True)

    with transaction.atomic():
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            logger.info(
                "Updated quantity for '%s' (ID: %s) in Cart ID: %s",
                product.title,
                product.id,
                cart.id,
            )
        else:
            cart_item.quantity = quantity
            logger.info(
                "Added new product '%s' (ID: %s) to Cart ID: %s",
                product.title,
                product.id,
                cart.id,
            )
        cart_item.save()

    total_items = sum(item.quantity for item in cart.items.all())
    counter_html = f"<span id='cart-counter' class='quantity'>{total_items}</span>"

    mini_cart_inner_html = render_to_string(
        "shop/includes/mini_cart.html", {"cart": cart}, request=request
    )
    oob_mini_cart = (
        f'<div id="mini-cart-container" class="mini-cart-dropdown" '
        f'hx-swap-oob="true">{mini_cart_inner_html}</div>'
    )

    response = HttpResponse(counter_html + oob_mini_cart)

    message = str(_("Товар успешно добавлен в корзину"))
    response["HX-Trigger"] = json.dumps({"showMessage": message, "cartUpdated": ""})

    return response


@router.post("/cart/item/{item_id}/update/")
def update_cart_item(request, item_id: int, action: str = Form(...)):
    """
    Increases or decreases the quantity of a specific cart item atomically.
    """
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    with transaction.atomic():
        if action == "increase":
            item.quantity += 1
            item.save()
            logger.debug(
                "Increased quantity to %s for CartItem ID: %s", item.quantity, item.id
            )
        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                logger.debug(
                    "Decreased quantity to %s for CartItem ID: %s",
                    item.quantity,
                    item.id,
                )
            else:
                item.delete()
                logger.info(
                    "Removed CartItem ID: %s because quantity reached 0", item.id
                )

    return get_cart_update_response(request, cart)


@router.post("/cart/item/{item_id}/remove/")
def remove_cart_item(request, item_id: int):
    """Removes an item from the cart completely (e.g., via cross button)."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()

    logger.info("Manually removed CartItem ID: %s from Cart ID: %s", item_id, cart.id)

    return get_cart_update_response(request, cart)
