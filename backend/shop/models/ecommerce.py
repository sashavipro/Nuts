"""shop/models/ecommerce.py."""
#
# from django.db import models
# from django.conf import settings
# from wagtail.models import Page
# from wagtail.fields import StreamField
# from wagtail.admin.panels import FieldPanel
# from contacts.blocks import ContactImportBlock
# from .products import Product
# from .snippets import DeliveryMethod, PaymentMethod
#
#
# class Cart(models.Model):
#     """Represents a shopping cart for a user or session."""
#
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
#     )
#     session_key = models.CharField(max_length=40, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class CartItem(models.Model):
#     """Represents a single product item within a shopping cart."""
#
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
#
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#
# class Order(models.Model):
#     """Represents a customer order containing products and delivery details."""
#
#     STATUS_CHOICES = [
#         ("new", "Новый"),
#         ("processing", "В обработке"),
#         ("completed", "Выполнен"),
#     ]
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="orders",
#     )
#     manager = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="managed_orders",
#     )
#
#     order_number = models.CharField(max_length=20, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
#
#     total_amount = models.DecimalField(max_digits=10, decimal_places=0)
#     items_count = models.PositiveIntegerField(default=0)
#
#     delivery_method = models.ForeignKey(
#         DeliveryMethod, on_delete=models.SET_NULL, null=True
#     )
#     payment_method = models.ForeignKey(
#         PaymentMethod, on_delete=models.SET_NULL, null=True
#     )
#
#     first_name = models.CharField(max_length=150)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     city = models.CharField(max_length=100, blank=True)
#     address_line = models.CharField(max_length=255, blank=True)
#
#
# class OrderItem(models.Model):
#     """Represents a specific product line item within an order."""
#
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(ProductPage, on_delete=models.SET_NULL, null=True)
#     product_name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=0)
#     quantity = models.PositiveIntegerField(default=1)
#
#
# class PaymentTransaction(models.Model):
#     """Records a payment transaction associated with a user."""
#
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="payment_transactions",
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, default="success")
#     description = models.CharField(max_length=255)
#
#
# class OrderSuccessPage(Page):
#     """Page displayed to the user after a successful order placement."""
#
#     background_image = models.ForeignKey(
#         "wagtailimages.Image", null=True, on_delete=models.SET_NULL, related_name="+"
#     )
#     footer_blocks = StreamField(
#         [
#             ("contacts_section", ContactImportBlock()),
#         ],
#         use_json_field=True,
#     )
#     content_panels = Page.content_panels + [
#         FieldPanel("background_image"),
#         FieldPanel("footer_blocks"),
#     ]
