"""Make talking to Yelp even easier."""

from yelpapi import YelpAPI

from django.conf import settings


def get_yelp_data(query: dict):
    """Query Yelp API for nearby businesses."""
    yelp = YelpAPI(settings.PLUGINS_CONFIG["nautobot_lunch"]["yelp_api_key"], timeout_s=3.0)

    return yelp.search_query(**query)
