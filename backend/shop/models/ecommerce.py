"""shop/models/ecommerce.py."""

import uuid
import logging
from django.db import models, transaction
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from contacts.blocks import ContactImportBlock
from home.blocks import HeroBlock
from .products import Product

# pylint: disable=no-member, too-few-public-methods, too-many-ancestors, cyclic-import, disable=duplicate-code

logger = logging.getLogger(__name__)


def get_or_create_cart(request):
    """
    Retrieves the existing cart or creates a new one.

    Uses the authenticated user if available; otherwise, uses the session key.
    """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            logger.debug(
                "Created new cart for authenticated user: %s", request.user.username
            )
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(
            session_key=session_key, user__isnull=True
        )
        if created:
            logger.debug("Created new cart for anonymous session: %s", session_key)
    return cart


class Cart(models.Model):
    """Represents a shopping cart tied to a user or a session."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Пользователь"),
    )
    session_key = models.CharField(
        _("Ключ сессии"), max_length=40, null=True, blank=True
    )
    created_at = models.DateTimeField(_("Создана"), auto_now_add=True)

    def get_total_price(self):
        """Calculates and returns the total price of all items in the cart."""
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        """String representation of the Cart."""
        return f"Cart {self.id} - User: {self.user or 'Anonymous'}"

    class Meta:
        """Meta options for the Cart model."""

        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")


class CartItem(models.Model):
    """Represents a single product entry with its quantity inside a Cart."""

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("Корзина")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Товар")
    )
    quantity = models.PositiveIntegerField(_("Количество"), default=1)

    def get_cost(self):
        """Calculates the total cost for this specific cart item."""
        return self.product.price * self.quantity

    def __str__(self):
        """String representation of the CartItem."""
        return f"{self.quantity} x {self.product.title}"

    class Meta:
        """Meta options for the CartItem model."""

        verbose_name = _("Элемент корзины")
        verbose_name_plural = _("Элементы корзины")


class Order(models.Model):
    """Represents a finalized customer order with billing and delivery details."""

    class Status(models.TextChoices):
        """Enumeration for order processing statuses."""

        NEW = "new", _("Новый")
        PROCESSING = "processing", _("В обработке")
        COMPLETED = "completed", _("Выполнен")

    class Delivery(models.TextChoices):
        """Enumeration for available delivery methods."""

        NOVA_POSHTA = (
            "nova_poshta",
            _("Новая почта (по Украине оплата за счет Клиента)"),
        )
        COURIER = "courier", _("Курьер по Одессе")
        PICKUP = "pickup", _("Самовывоз со склада")

    class Payment(models.TextChoices):
        """Enumeration for available payment methods."""

        INVOICE = "invoice", _("Безналичный расчет")
        CARD = "card", _("LiqPay / Приват24")
        CASH = "cash", _("Наличными при получении (Наложенным платежом)")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name=_("Пользователь"),
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_orders",
        verbose_name=_("Менеджер"),
    )

    order_number = models.CharField(_("Номер заказа"), max_length=20, unique=True)
    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)
    status = models.CharField(
        _("Статус"), max_length=20, choices=Status.choices, default=Status.NEW
    )
    total_amount = models.DecimalField(_("Сумма"), max_digits=10, decimal_places=0)
    items_count = models.PositiveIntegerField(_("Количество товаров"), default=0)

    delivery_method = models.CharField(
        _("Способ доставки"),
        max_length=20,
        choices=Delivery.choices,
        default=Delivery.NOVA_POSHTA,
    )
    payment_method = models.CharField(
        _("Способ оплаты"), max_length=20, choices=Payment.choices, default=Payment.CARD
    )

    first_name = models.CharField(_("Имя"), max_length=150)
    phone = models.CharField(_("Телефон"), max_length=20)
    email = models.EmailField(_("Email"))

    city = models.CharField(_("Город"), max_length=100, blank=True)
    address_line = models.CharField(_("Адрес/Отделение"), max_length=255, blank=True)
    company_name = models.CharField(_("Название компании"), max_length=255, blank=True)
    okpo = models.CharField(_("ОКПО"), max_length=20, blank=True)

    def __str__(self):
        """String representation of the Order."""
        return f"Order {self.order_number} ({self.get_status_display()})"

    class Meta:
        """Meta options for the Order model."""

        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        ordering = ["-created_at"]


class OrderItem(models.Model):
    """Represents a snapshot of a product within a finalized order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, verbose_name=_("Товар")
    )
    product_name = models.CharField(
        _("Название товара (на момент заказа)"), max_length=255
    )
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(_("Количество"), default=1)

    def __str__(self):
        """String representation of the OrderItem."""
        return (
            f"{self.quantity} x {self.product_name} (Order: {self.order.order_number})"
        )

    class Meta:
        """Meta options for the OrderItem model."""

        verbose_name = _("Товар в заказе")
        verbose_name_plural = _("Товары в заказе")


class PaymentTransaction(models.Model):
    """Records a payment event associated with a user and potentially an order."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payment_transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="success")
    description = models.CharField(max_length=255)

    def __str__(self):
        """String representation of the PaymentTransaction."""
        return f"Transaction {self.id} - {self.amount} by {self.user}"


class CartPage(Page):
    """Wagtail page representing the shopping cart view."""

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["shop.CheckoutPage"]
    template = "shop/cart.html"

    manager_title = models.CharField(
        max_length=255,
        default=_("Ваш личный менеджер Олег"),
        verbose_name=_("Текст 'Личный менеджер'"),
    )
    manager_phone = models.CharField(
        max_length=50, default="+38 067 777 14 12", verbose_name=_("Телефон менеджера")
    )

    content_panels = Page.content_panels + [
        FieldPanel("manager_title"),
        FieldPanel("manager_phone"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Injects the current user's cart into the template context."""
        context = super().get_context(request, *args, **kwargs)
        context["cart"] = get_or_create_cart(request)
        return context


class CheckoutPage(Page):
    """Wagtail page handling the checkout process and order creation."""

    max_count = 1
    parent_page_types = ["shop.CartPage"]
    subpage_types = ["shop.OrderSuccessPage"]
    template = "shop/checkout.html"

    def serve(self, request, *args, **kwargs):
        """
        Processes the checkout form submission.

        Uses transaction.atomic() to ensure the order, its items, and the cart
        clearing happen as a single, indivisible database operation.
        """
        # pylint: disable=import-outside-toplevel
        from shop.forms import CheckoutForm

        cart = get_or_create_cart(request)

        if not cart.items.exists():
            logger.warning("Attempted checkout with an empty cart.")
            messages.warning(request, _("Ваша корзина пуста."))
            return redirect(self.get_parent().url)

        if request.method == "POST":
            form = CheckoutForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        order = form.save(commit=False)

                        if request.user.is_authenticated:
                            order.user = request.user

                        order.total_amount = cart.get_total_price()
                        order.items_count = sum(
                            item.quantity for item in cart.items.all()
                        )
                        order.order_number = f"ORD-{uuid.uuid4().hex[:6].upper()}"
                        order.save()

                        for item in cart.items.all():
                            OrderItem.objects.create(
                                order=order,
                                product=item.product,
                                product_name=item.product.title,
                                price=item.product.price,
                                quantity=item.quantity,
                            )

                        cart.items.all().delete()

                    logger.info(
                        "Order %s successfully created for user %s.",
                        order.order_number,
                        request.user,
                    )
                    request.session["last_order_id"] = order.order_number

                    if order.payment_method == Order.Payment.CARD:
                        return redirect("mock_payment", order_number=order.order_number)

                    success_page = OrderSuccessPage.objects.live().first()
                    if success_page:
                        return redirect(success_page.url)

                    messages.success(request, _("Заказ успешно оформлен!"))
                    return redirect("/")

                except Exception as e:  # pylint: disable=broad-exception-caught
                    logger.error(
                        "Failed to create order due to a database error: %s", e
                    )
                    messages.error(
                        request,
                        _(
                            "Произошла ошибка при оформлении заказа. "
                            "Попробуйте еще раз."
                        ),
                    )
            else:
                logger.warning("Checkout form validation failed: %s", form.errors)
        else:
            initial_data = {}
            if request.user.is_authenticated:
                initial_data = {
                    "first_name": f"{request.user.first_name} {request.user.last_name}".strip(),
                    "phone": getattr(request.user, "phone", ""),
                    "email": request.user.email,
                    "city": getattr(request.user, "city", ""),
                    "address_line": getattr(request.user, "address_line", ""),
                    "company_name": getattr(request.user, "company_name", ""),
                    "okpo": getattr(request.user, "okpo", ""),
                }
            form = CheckoutForm(initial=initial_data)

        context = self.get_context(request, *args, **kwargs)
        context["form"] = form
        context["cart"] = cart
        return render(request, self.template, context)


class OrderSuccessPage(Page):
    """Wagtail page displayed after a successful checkout."""

    max_count = 1
    parent_page_types = ["shop.CheckoutPage"]
    subpage_types = []

    body = StreamField(
        [("hero", HeroBlock())],
        use_json_field=True,
        blank=True,
        verbose_name=_("Баннер (Hero)"),
    )

    footer_blocks = StreamField(
        [("contacts_section", ContactImportBlock())],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("footer_blocks"),
    ]
