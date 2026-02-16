"""shop/models/products.py."""

from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from home.blocks import AboutBlock
from contacts.blocks import ContactImportBlock


class ShopIndexPage(Page):  # pylint: disable=too-many-ancestors
    """The main catalog page listing products."""

    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, on_delete=models.SET_NULL, related_name="+"
    )
    body = StreamField(
        [
            ("seo_block", AboutBlock()),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("body"),
    ]
    subpage_types = ["ProductPage"]


class ProductPage(Page):  # pylint: disable=too-many-ancestors
    """Page model representing a single product."""

    sku = models.CharField("Артикул", max_length=50)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=0)
    old_price = models.DecimalField(
        "Старая цена", max_digits=10, decimal_places=0, blank=True, null=True
    )
    short_description = models.TextField("Краткое описание")

    weight_grams = models.PositiveIntegerField("Вес (число)", default=40)
    weight_details = models.CharField("Вес (строка)", max_length=50, default="40г.")
    tastes = ParentalManyToManyField("ProductTaste", blank=True)
    packaging = models.ForeignKey(
        "ProductPackaging", on_delete=models.SET_NULL, null=True, blank=True
    )

    composition = models.TextField("Состав", blank=True)
    energy_value = models.CharField("Энерг. ценность", max_length=100, blank=True)
    shelf_life = models.CharField("Срок годности", max_length=255, blank=True)
    storage_conditions = models.TextField("Условия хранения", blank=True)

    # Табы
    description = RichTextField("Описание")
    packaging_info = RichTextField("Упаковка", blank=True)
    payment_info = RichTextField("Оплата", blank=True)
    delivery_info = RichTextField("Доставка", blank=True)

    is_new = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("sku"), FieldPanel("price"), FieldPanel("old_price")],
            heading="Торговое",
        ),
        FieldPanel("short_description"),
        InlinePanel("gallery_images", label="Галерея"),
        MultiFieldPanel(
            [FieldPanel("weight_grams"), FieldPanel("tastes"), FieldPanel("packaging")],
            heading="Фильтры",
        ),
        MultiFieldPanel(
            [
                FieldPanel("composition"),
                FieldPanel("weight_details"),
                FieldPanel("energy_value"),
            ],
            heading="Спецификация",
        ),
        MultiFieldPanel(
            [FieldPanel("description"), FieldPanel("packaging_info")], heading="Контент"
        ),
        MultiFieldPanel(
            [FieldPanel("is_new"), FieldPanel("is_sale")], heading="Бейджи"
        ),
    ]
    parent_page_types = ["ShopIndexPage"]

    def main_image(self):
        """Retrieve the first image from the product gallery."""
        item = self.gallery_images.first()  # pylint: disable=no-member
        return item.image if item else None


class ProductGalleryImage(Orderable):
    """An image for the product gallery, linked to a ProductPage."""

    page = ParentalKey(
        ProductPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(max_length=250, blank=True)
    panels = [FieldPanel("image"), FieldPanel("caption")]
