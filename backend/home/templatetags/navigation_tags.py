"""home/templatetags/navigation_tags.py."""

from django import template
from wagtail.models import Page, Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Возвращает корневую страницу текущего сайта."""
    return Site.find_for_request(context["request"]).root_page


@register.simple_tag(takes_context=True)
def get_top_menu(context):
    """
    Возвращает элементы меню (дочерние страницы корня),
    у которых стоит галочка 'Show in menus'.
    """
    site_root = get_site_root(context)
    return site_root.get_children().live().in_menu()


@register.inclusion_tag("includes/breadcrumbs.html", takes_context=True)
def breadcrumbs(context, is_hero=False):
    """
    Рендерит хлебные крошки.
    """
    # Берем страницу из контекста. В Wagtail она обычно называется 'page'.
    # 'self' внутри блока StreamField - это сам блок, а не страница.
    page = context.get("page")

    # Проверка на то, что это действительно страница Wagtail
    if not isinstance(page, Page) or page.depth <= 2:
        ancestors = []
    else:
        # Получаем предков
        ancestors = Page.objects.ancestor_of(page, inclusive=True).filter(depth__gt=1)

    return {
        "ancestors": ancestors,
        "request": context.get("request"),
        "is_hero": is_hero,
    }


@register.simple_tag(takes_context=True)
def has_hero_block(context):
    """
    Проверяет, есть ли в body страницы блок 'hero'.
    Нужен, чтобы не дублировать крошки.
    """
    page = context.get("page")
    if not page or not hasattr(page, "body"):
        return False

    for block in page.body:
        if block.block_type == "hero":
            return True
    return False
