"""App declaration for nautobot_lunch."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

import os

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class LunchConfig(NautobotAppConfig):
    """App configuration for the nautobot_lunch app."""

    name = "nautobot_lunch"
    verbose_name = "Nautobot Lunch"
    version = __version__
    author = "Nate Gotz"
    description = "Nautobot Lunch."
    base_url = "lunch"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {
        "yelp_api_key": os.getenv("YELP_API_KEY", ""),
        "cache_time": os.getenv("NAUTOBOT_LUNCH_CACHE_TIME", "3600"),
    }


config = LunchConfig  # pylint:disable=invalid-name
