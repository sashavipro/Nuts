"""users/api.py."""

import logging

from cities_light.models import Region
from django.http import HttpRequest
from ninja import NinjaAPI, Schema

logger = logging.getLogger(__name__)
api = NinjaAPI()


class RegionSchema(Schema):
    """Schema for serializing Region data."""

    id: int
    name: str


@api.get("/regions", response=list[RegionSchema])
def get_regions(request: HttpRequest, country_id: int):  # pylint: disable=unused-argument
    """Retrieve a list of regions for a specific country."""
    logger.debug("API Request: Fetching regions for country_id=%s", country_id)

    regions = Region.objects.filter(country_id=country_id).order_by("name")

    if not regions.exists():
        logger.info("No regions found for country_id=%s", country_id)

    return regions
