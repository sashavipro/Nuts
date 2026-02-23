"""shop/urls.py."""

from django.urls import path
from ninja import NinjaAPI
from .api import router as shop_router
from . import views

api = NinjaAPI(urls_namespace="shop_api", title="Shop API", docs_url="/docs/")


api.add_router("/", shop_router)

urlpatterns = [
    path("api/", api.urls),
    path("payment/<str:order_number>/", views.mock_payment, name="mock_payment"),
]
