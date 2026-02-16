"""users/urls.py."""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users.api import api as user_api

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("api/", user_api.urls),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html", next_page="/"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
