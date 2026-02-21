"""users/admin.py"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import CustomUser

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Registering a custom user model using Unfold styles.
    """

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    # pylint: disable=duplicate-code
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            _("Дополнительная информация"),
            {
                "fields": (
                    "user_type",
                    "is_fop",
                    "middle_name",
                    "phone",
                    "company_name",
                    "okpo",
                    "country",
                    "region",
                    "city",
                    "address_line",
                    "zip_code",
                ),
            },
        ),
    )


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """
    Registering group models using Unfold styles.
    """
