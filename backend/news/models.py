"""news/models.py."""

import logging
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
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

    date = models.DateField("Publication Date")
    is_wide_display = models.BooleanField(
        "Full Width (Wide)?",
        default=False,
        help_text="If checked, the news item will occupy the full width"
        " (col-12) in the list.",
    )

    show_text_on_preview = models.BooleanField(
        "Show Title/Intro over Preview?",
        default=False,
        help_text="If checked: Title and Intro will be centered over the image/video"
        " (white text). If unchecked: below the image (black text).",
    )

    intro = models.TextField(
        "Short Description", help_text="For the news list", blank=True
    )

    preview_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Preview: Image",
    )
    preview_video = models.ForeignKey(
        "wagtailmedia.Media",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Preview: Video",
    )

    body = StreamField(
        [
            (
                "rich_text",
                blocks.RichTextBlock(
                    label="Text Block",
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
            ("media_block", MediaOverlayBlock(label="Media (Photo/Video) + Text")),
            ("eco_banner", EcoBannerBlock(label="Eco Banner")),
        ],
        use_json_field=True,
        verbose_name="Content Constructor",
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
            heading="Preview Settings",
        ),
        FieldPanel("body", heading="News Content"),
    ]

    parent_page_types = ["news.NewsIndexPage"]
    subpage_types = []

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options for NewsPage."""

        verbose_name = "News Page"
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

    custom_title = models.CharField("H1 Title", max_length=255, blank=True)
    intro = models.TextField("Section Description", blank=True)
    news_per_page = models.IntegerField("News per page", default=6)
    recent_news_count = models.IntegerField("Sidebar recent news count", default=3)

    sidebar_widget = StreamField(
        [
            ("social_widget", SidebarSocialBlock()),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Sidebar Social Widget",
    )

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
            heading="Sidebar Settings",
        ),
        FieldPanel("footer_blocks"),
    ]

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
