"""news/models.py."""

import logging
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail import blocks
from home.blocks import EcoBannerBlock
from news.blocks import MediaOverlayBlock, SidebarSocialBlock
from contacts.blocks import ContactImportBlock

logger = logging.getLogger(__name__)


class NewsPage(Page):  # pylint: disable=too-many-ancestors
    """
    Page model representing a single News Article.
    Contains preview settings for the list view and a StreamField for the main content.
    """

    date = models.DateField(_("Дата публикации"))
    is_wide_display = models.BooleanField(
        _("Полная ширина (широкий)?"),
        default=False,
        help_text=_(
            "Если этот флажок установлен,"
            " новость будет занимать всю ширину (col-12) в списке."
        ),
    )

    show_text_on_preview = models.BooleanField(
        _("Показать название/вступление над превью?"),
        default=False,
        help_text=_(
            "Если флажок установлен: заголовок и введение будут"
            " выровнены по центру над изображением/видео (белый текст)."
            " Если флажок не установлен: под изображением (черный текст)."
        ),
    )

    intro = models.TextField(
        _("Краткое описание"), help_text=_("Для списка новостей"), blank=True
    )

    # pylint: disable=duplicate-code
    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Предварительный просмотр: Изображение"),
    )
    # pylint: enable=duplicate-code

    preview_video = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name=_("Предварительный просмотр: Видео"),
    )

    body = StreamField(
        [
            (
                "rich_text",
                blocks.RichTextBlock(
                    label=_("Текстовый блок"),
                    features=[
                        "h2",
                        "h3",
                        "h4",
                        "bold",
                        "italic",
                        "link",
                        "ol",
                        "ul",
                        "hr",
                    ],
                ),
            ),
            ("media_block", MediaOverlayBlock(label=_("Медиа (фото/видео) + текст"))),
            ("eco_banner", EcoBannerBlock(label=_("Эко-баннер"))),
        ],
        use_json_field=True,
        verbose_name=_("Конструктор контента"),
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        MultiFieldPanel(
            [
                FieldPanel("is_wide_display"),
                FieldPanel("show_text_on_preview"),
                FieldPanel("intro"),
                FieldPanel("preview_image"),
                FieldPanel("preview_video"),
            ],
            heading=_("Настройки предварительного просмотра"),
        ),
        FieldPanel("body", heading=_("Новости Содержание")),
    ]

    parent_page_types = ["news.NewsIndexPage"]
    subpage_types = []

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options for NewsPage."""

        verbose_name = _("Страница новостей")
        ordering = ["-date"]

    def get_recent_news(self):
        """
        Retrieves recent news items to display in the sidebar.
        The count is determined by the parent NewsIndexPage settings.
        """
        parent = self.get_parent().specific
        count = getattr(parent, "recent_news_count", 3)
        # pylint: disable=no-member
        return (
            NewsPage.objects.live()
            .sibling_of(self)
            .exclude(id=self.id)
            .order_by("-date")[:count]
        )


class NewsIndexPage(Page):  # pylint: disable=too-many-ancestors
    """
    Index page for News.
    Displays a list of NewsPage children with pagination and HTMX support.
    """

    custom_title = models.CharField(_("H1 Заголовок"), max_length=255, blank=True)
    intro = models.TextField(_("Описание раздела"), blank=True)
    news_per_page = models.IntegerField(_("Новости на странице"), default=6)
    recent_news_count = models.IntegerField(
        _("Количество последних новостей в боковой панели"), default=3
    )

    sidebar_widget = StreamField(
        [
            ("social_widget", SidebarSocialBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name=_("Социальный виджет боковой панели"),
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
        FieldPanel("custom_title"),
        FieldPanel("intro"),
        FieldPanel("news_per_page"),
        MultiFieldPanel(
            [
                FieldPanel("recent_news_count"),
                FieldPanel("sidebar_widget"),
            ],
            heading=_("Настройки боковой панели"),
        ),
        FieldPanel("footer_blocks"),
    ]
    # pylint: enable=duplicate-code

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["news.NewsPage"]

    def get_context(self, request, *args, **kwargs):
        """
        Adds paginated news items to the context.
        """
        context = super().get_context(request, *args, **kwargs)
        all_news = NewsPage.objects.live().child_of(self).order_by("-date")
        paginator = Paginator(all_news, self.news_per_page)
        page = request.GET.get("page")

        try:
            news_items = paginator.page(page)
        except PageNotAnInteger:
            news_items = paginator.page(1)
        except EmptyPage:
            news_items = paginator.page(paginator.num_pages)

        context["news_items"] = news_items
        return context

    def serve(self, request, *args, **kwargs):
        """
        Handles requests. Intercepts HTMX requests to return the partial list.
        """
        if request.headers.get("HX-Request"):
            # pylint: disable=no-member
            logger.info(
                "HTMX Request detected on NewsIndexPage %s. Page: %s",
                self.id,
                request.GET.get("page"),
            )
            context = self.get_context(request, *args, **kwargs)
            return TemplateResponse(request, "news/includes/news_list.html", context)

        return super().serve(request, *args, **kwargs)
