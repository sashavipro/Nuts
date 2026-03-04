"""core/admin.py."""

from django.contrib import admin

original_get_app_list = admin.site.get_app_list


def custom_get_app_list(request, app_label=None):
    """custom_get_app_list"""
    app_list = original_get_app_list(request, app_label)
    hidden_apps = [
        "cities_light",
        "wagtailmedia",
        "wagtaildocs",
        "wagtailimages",
        "taggit",
    ]
    return [app for app in app_list if app.get("app_label") not in hidden_apps]


admin.site.get_app_list = custom_get_app_list
