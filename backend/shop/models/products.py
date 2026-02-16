"""shop/models/products.py."""

import logging

from django.core.exceptions import ValidationError
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Locale, Orderable, Page

from contacts.blocks import ContactImportBlock
from home.blocks import EcoBannerBlock
from shop.blocks import (
    IconTextBlock,
    PriceBlock,
    ProductAttributeBlock,
    ProductTabsBlock,
    SkuBlock,
)
from .snippets import ProductPackaging, ProductTaste, ProductWeight

logger = logging.getLogger(__name__)


class ProductPageForm(WagtailAdminPageForm):  # pylint: disable=too-many-ancestors
    """
    Custom form for ProductPage to manage the product selection field.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set the queryset for the product field to include all products.
        """
        super().__init__(*args, **kwargs)
        # pylint: disable=no-member
        products = Product.objects.all()
        self.fields["product"].queryset = products
        logger.debug("ProductPageForm initialized with %d products.", products.count())


class ProductPage(Page):  # pylint: disable=too-many-ancestors
    """
    Represents a product detail page in the Wagtail CMS tree.
    Links a Product model instance to a specific URL within a specific Locale.
    """

    base_form_class = ProductPageForm

    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.PROTECT,
        related_name="pages",
        verbose_name="Товар из базы данных",
    )

    custom_description = models.TextField(
        "Кастомное описание (перекрывает базу)", blank=True
    )

    body = StreamField(
        [
            ("tabs_section", ProductTabsBlock()),
            ("contacts_section", ContactImportBlock()),
            ("rich_text", blocks.RichTextBlock(label="Текст")),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Основной контент (снизу)",
    )

    content_blocks = StreamField(
        [
            ("sku_block", SkuBlock()),
            ("attribute_block", ProductAttributeBlock()),
            ("icon_text_block", IconTextBlock()),
            ("price_block", PriceBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Конструктор правой колонки",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("product"),
            ],
            heading="Связь с товаром",
        ),
        FieldPanel("content_blocks"),
        FieldPanel("body"),
    ]

    parent_page_types = ["shop.ShopIndexPage"]
    subpage_types = []

    def clean(self):
        """
        Validates that a page for the selected product does not already exist
        within the current locale to prevent duplicate pages.
        """
        super().clean()
        # pylint: disable=no-member
        if self.product:
            existing_pages = ProductPage.objects.filter(
                product=self.product, locale=self.locale
            )

            if self.pk:
                existing_pages = existing_pages.exclude(pk=self.pk)

            if existing_pages.exists():
                logger.warning(
                    "Duplicate ProductPage attempted for product '%s' in locale '%s'.",
                    self.product.title,
                    self.locale,
                )
                raise ValidationError(
                    {
                        "product": f"Ошибка: Для товара '{self.product.title}' уже"
                        f" создана страница на этом языке ({self.locale})."
                    }
                )

    def get_context(self, request, *args, **kwargs):
        """
        Adds the associated product and related products to the template context.
        """
        context = super().get_context(request, *args, **kwargs)
        context["product"] = self.product
        # pylint: disable=no-member
        context["related_products"] = Product.objects.filter(live=True).exclude(
            id=self.product.id
        )[:4]
        logger.debug("Context prepared for ProductPage '%s'.", self.title)
        return context


class ProductGalleryImage(Orderable):  # pylint: disable=too-few-public-methods
    """
    Represents an image within a product's gallery, allowing for custom ordering.
    """

    product = ParentalKey(
        "shop.Product", on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name="Изображение",
    )
    caption = models.CharField("Подпись", max_length=255, blank=True)
    position = models.IntegerField(
        "Позиция (0 = главная)",
        default=0,
        help_text="0 = первая/главная, 10 = вторая, 20 = третья и т.д.",
    )

    panels = [
        FieldPanel("image"),
        FieldPanel("position"),
        FieldPanel("caption"),
    ]

    class Meta:
        """
        Meta options for ProductGalleryImage.
        """

        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"
        ordering = ["position"]

    def save(self, *args, **kwargs):
        """
        Overrides the save method to synchronize the sort_order field.
        """
        self.sort_order = self.position
        super().save(*args, **kwargs)


class Product(ClusterableModel):  # pylint: disable=too-few-public-methods
    """
    Represents a specific product entity in the database, managed via the admin panel.
    """

    title = models.CharField("Название товара", max_length=255)
    slug = models.SlugField(
        "URL (slug)",
        unique=True,
        allow_unicode=True,
        help_text="Часть ссылки, например: greckiy-oreh",
    )

    sku = models.CharField("Артикул", max_length=50, blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=0)
    old_price = models.DecimalField(
        "Старая цена", max_digits=10, decimal_places=0, null=True, blank=True
    )

    weight_option = models.ForeignKey(
        "shop.ProductWeight",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Вес",
        related_name="products",
    )

    energy_value = models.CharField(
        "Энерг. ценность", max_length=255, blank=True, default="654 Ккал."
    )
    shelf_life = models.CharField("Срок годности", max_length=255, blank=True)
    composition = models.TextField("Состав", blank=True)

    tastes = models.ManyToManyField(ProductTaste, blank=True, verbose_name="Вкусы")
    packaging = models.ForeignKey(
        ProductPackaging,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Упаковка",
    )

    is_new = models.BooleanField("Новинка", default=False)
    is_sale = models.BooleanField("Акция", default=False)
    live = models.BooleanField("Опубликовано", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta options for Product.
        """

        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("sku"),
        FieldPanel("price"),
        FieldPanel("old_price"),
        FieldPanel("weight_option"),
        FieldPanel("energy_value"),
        FieldPanel("shelf_life"),
        FieldPanel("composition"),
        FieldPanel("tastes"),
        FieldPanel("packaging"),
        FieldPanel("is_new"),
        FieldPanel("is_sale"),
        FieldPanel("live"),
        InlinePanel("gallery_images", label="Галерея изображений (первое = главное)"),
    ]

    def __str__(self):
        """
        Returns the string representation of the product (its title).
        """
        return str(self.title)

    def get_gallery_images(self):
        """
        Retrieves all gallery images associated with this product.
        """
        # pylint: disable=no-member
        return self.gallery_images.all()

    def get_main_image(self):
        """
        Retrieves the first image from the gallery to serve as the main product image.
        """
        # pylint: disable=no-member
        first = self.gallery_images.first()
        return first.image if first else None

    @property
    def page(self):
        """
        Retrieves the ProductPage associated with this product for the currently active locale.
        Falls back to the first available page if no localized page is found.
        """
        try:
            current_locale = Locale.get_active()
            # pylint: disable=no-member
            page = self.pages.filter(locale=current_locale).first()

            if not page:
                logger.warning(
                    "No specific ProductPage found for product '%s' in locale '%s'."
                    " Returning first available.",
                    self.title,
                    current_locale,
                )
                page = self.pages.first()

            return page
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error retrieving page for product '%s': %s", self.title, e)
            return None


class ShopIndexPage(RoutablePageMixin, Page):  # pylint: disable=too-many-ancestors
    """
    Represents the main catalog page, handling product listing, filtering, sorting, and pagination.
    """

    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero изображение",
    )
    custom_title = models.CharField(
        "Заголовок для Hero",
        max_length=255,
        blank=True,
        help_text="Если не заполнено, используется обычный title",
    )

    # pylint: disable=duplicate-code
    footer_blocks = StreamField(
        [
            ("eco", EcoBannerBlock()),
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_image"),
        FieldPanel("custom_title"),
        FieldPanel("footer_blocks"),
    ]
    # pylint: enable=duplicate-code

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["shop.ProductPage"]
    template = "shop/shop_index_page.html"
    ajax_template = "shop/includes/product_list.html"

    def get_context(self, request, *args, **kwargs):
        """
        Builds the context for the template, applying filters (taste, weight),
        sorting, and pagination to the product list.
        """
        context = super().get_context(request, *args, **kwargs)
        # pylint: disable=no-member
        products = Product.objects.filter(live=True)

        taste_id = request.GET.get("taste")
        if taste_id:
            products = products.filter(tastes__id=taste_id)
            context["current_taste"] = int(taste_id)

        weight_id = request.GET.get("weight")
        if weight_id:
            products = products.filter(weight_option__id=weight_id)
            context["current_weight"] = int(weight_id)

        sort_val = request.GET.get("sort")
        if sort_val == "price_asc":
            products = products.order_by("price")
            context["current_sort"] = "price_asc"
        elif sort_val == "price_desc":
            products = products.order_by("-price")
            context["current_sort"] = "price_desc"
        elif sort_val == "new":
            products = products.filter(is_new=True).order_by("-created_at")
            context["current_sort"] = "new"
        else:
            products = products.order_by("-created_at")
            context["current_sort"] = "default"

        paginator = Paginator(products, 9)
        page = request.GET.get("page")
        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        context["products"] = products_page
        context["tastes"] = ProductTaste.objects.all()
        context["weights"] = ProductWeight.objects.all()
        logger.debug(
            "ShopIndexPage context built. Products count: %d, Sort: %s",
            len(products_page),
            sort_val,
        )
        return context

    def serve(self, request, *args, **kwargs):
        """
        Handles the request, supporting HTMX for partial updates of the product list.
        """
        if request.headers.get("HX-Request") == "true":
            logger.info("Handling HTMX request for ShopIndexPage.")
            context = self.get_context(request, *args, **kwargs)
            return TemplateResponse(request, self.ajax_template, context)
        return super().serve(request, *args, **kwargs)

    @route(r"^([^/]+)/$")
    def product_detail(self, request, slug):
        """
        Routable page view that handles product detail URLs based on the product slug.
        Redirects to the specific ProductPage associated with the slug.
        """
        logger.debug("Attempting to serve product detail for slug: %s", slug)
        # pylint: disable=no-member
        product = get_object_or_404(Product, slug=slug, live=True)
        actual_page = product.page

        if actual_page and actual_page.live:
            logger.info(
                "Serving ProductPage '%s' for product '%s'.",
                actual_page.title,
                product.title,
            )
            return render(
                request,
                "shop/product_page.html",
                {
                    "page": actual_page,
                    "product": product,
                },
            )

        logger.warning(
            "No active ProductPage found for product '%s'. Fallback to ShopIndexPage.",
            product.title,
        )
        return render(
            request,
            "shop/product_page.html",
            {
                "page": self,
                "product": product,
            },
        )
