"""shop/models/products.py."""

import logging

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import StreamField
from wagtail.models import Locale, Orderable, Page

from contacts.blocks import ContactImportBlock
from home.blocks import EcoBannerBlock, HeroBlock
from shop.blocks import ProductTabsBlock
from .snippets import ProductPackaging, ProductTaste, ProductWeight

logger = logging.getLogger(__name__)


class ProductPage(Page):  # pylint: disable=too-many-ancestors
    """
    A Wagtail Page model serving as a global template for individual product detail views.

    It is restricted to a single instance (max_count = 1) and provides common
    elements like global tabs and footers across all products in the catalog.
    """

    max_count = 1

    body = StreamField(
        [
            ("tabs_section", ProductTabsBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name=_("Общие табы для всех товаров"),
    )

    footer_blocks = StreamField(
        [
            ("contacts_section", ContactImportBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name=_("Подвал (контакты)"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
        FieldPanel("footer_blocks"),
    ]

    parent_page_types = ["shop.ShopIndexPage"]
    subpage_types = []


class ProductGalleryImage(Orderable):  # pylint: disable=too-few-public-methods
    """
    Represents an orderable image within a product's gallery.
    """

    product = ParentalKey(
        "shop.Product", on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Изображение"),
    )

    panels = [
        FieldPanel("image"),
    ]

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta options for the ProductGalleryImage model.
        """

        verbose_name = _("Изображение галереи")
        verbose_name_plural = _("Изображения галереи")


class Product(ClusterableModel):  # pylint: disable=too-few-public-methods
    """
    Represents a specific product entity in the e-commerce database, managed via the admin panel.
    """

    title = models.CharField(_("Название товара"), max_length=255)
    slug = models.SlugField(
        _("URL (slug)"),
        unique=True,
        allow_unicode=True,
        help_text=_("Часть ссылки, например: greckiy-oreh"),
    )

    sku = models.CharField(_("Артикул"), max_length=50, blank=True)
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=0)
    old_price = models.DecimalField(
        _("Старая цена"), max_digits=10, decimal_places=0, null=True, blank=True
    )

    weight_option = models.ForeignKey(
        "shop.ProductWeight",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Вес"),
        related_name="products",
    )

    energy_value = models.CharField(
        _("Энерг. ценность"), max_length=255, blank=True, default=_("654 Ккал.")
    )
    shelf_life = models.CharField(_("Срок годности"), max_length=255, blank=True)
    composition = models.TextField(_("Состав"), blank=True)

    storage_conditions = models.TextField(
        _("Условия хранения"), blank=True, default=_("Хранить в помещениях при...")
    )

    tastes = models.ManyToManyField(ProductTaste, blank=True, verbose_name=_("Вкусы"))
    packaging = models.ForeignKey(
        ProductPackaging,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Упаковка"),
    )

    is_new = models.BooleanField(_("Новинка"), default=False)
    is_sale = models.BooleanField(_("Акция"), default=False)
    live = models.BooleanField(_("Опубликовано"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta options for the Product model.
        """

        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")
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
        FieldPanel("storage_conditions"),
        FieldPanel("tastes"),
        FieldPanel("packaging"),
        FieldPanel("is_new"),
        FieldPanel("is_sale"),
        FieldPanel("live"),
        InlinePanel("gallery_images", label=_("Галерея изображений")),
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
        Retrieves the first image from the product's gallery to serve as the main display image.
        """
        # pylint: disable=no-member
        first = self.gallery_images.first()
        return first.image if first else None


class ShopIndexPage(RoutablePageMixin, Page):  # pylint: disable=too-many-ancestors
    """
    Represents the main catalog page, handling product listing, filtering,
    sorting, pagination, and dynamic routing for individual product detail views.
    """

    body = StreamField(
        [
            ("hero", HeroBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name=_("Контент страницы (сверху)"),
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

    products_per_page = models.PositiveIntegerField(
        default=9,
        verbose_name=_("Товаров на страницу"),
        help_text=_(
            "Укажите, сколько товаров показывать"
            " изначально и при нажатии 'Показать еще'"
        ),
    )

    content_panels = Page.content_panels + [
        FieldPanel("products_per_page"),
        FieldPanel("body"),
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

        paginator = Paginator(products, self.products_per_page)
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
        Handles the incoming request, supporting HTMX for partial DOM updates
        of the product list.
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

        Resolves the specific Product instance from the database and binds it
        to the global ProductPage template to render the product detail view.
        """
        logger.debug("Attempting to serve product detail for slug: %s", slug)

        # pylint: disable=no-member
        product = get_object_or_404(Product, slug=slug, live=True)

        current_locale = Locale.get_active()
        product_page_template = ProductPage.objects.filter(
            locale=current_locale
        ).first()

        if not product_page_template:
            product_page_template = ProductPage.objects.first()

        return render(
            request,
            "shop/product_page.html",
            {
                "page": product_page_template,
                "product": product,
            },
        )
