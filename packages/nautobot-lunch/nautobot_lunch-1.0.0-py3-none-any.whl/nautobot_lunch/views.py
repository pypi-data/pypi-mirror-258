"""Nautobot Lunch Views."""

import urllib.parse
from django.core.cache import cache
from django.conf import settings

from nautobot.apps import views
from nautobot.dcim.models import Location

from nautobot_lunch.yelp import get_yelp_data


def add_result_detail(results: list, location):
    """Add extra information used by the results to make a nice display."""
    for result in results:
        # Convert meters to miles
        result["distance_miles"] = round(result["distance"] * 0.000621371, 2)
        result["distance_kilometers"] = round(result["distance"] / 1000, 2)

        origin = f"{location.latitude},{location.longitude}"
        if location.physical_address:
            origin = urllib.parse.quote(location.physical_address.strip())

        destination = f"{result['coordinates']['latitude']},{result['coordinates']['longitude']}"

        # Create directions url with Google Maps
        directions_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"
        result["address"] = "<span>"
        result["address"] += "<br />".join(result["location"]["display_address"])
        result["address"] += f'<br /><a href="{directions_url}" target="_blank">Directions</a></span>'
    return results


def get_lunch_context(term: str, location, **kwargs):
    """Get Nearby lunch possibilities."""
    category = kwargs.get("category", "restaurants")

    params = {"term": term, "categories": category, "sort_by": "distance"}
    if location.physical_address:
        params["location"] = location.physical_address

    elif location.latitude and location.longitude:
        params["latitude"] = location.latitude
        params["longitude"] = location.longitude

    else:
        params = {}

    context = {"site": location}
    if bool(params):
        context["results"] = get_yelp_data(params)["businesses"]
    else:
        context["error"] = f"No location information provided for {location.name}."

    if "results" in context and len(context["results"]) > 0:
        context["results"] = add_result_detail(context["results"], location)

    return context


class LocationDetailPluginLunchTab(views.ObjectView):
    """View for displaying where to get lunch."""

    queryset = Location.objects.all()
    template_name = "nautobot_lunch/lunch_tab.html"

    def get_extra_context(self, request, instance):
        """Read request into a view that displays closest lunch places according to yelp."""
        query = request.GET.get("q", "")
        # Cache the query results for the defined amount of seconds
        cache_time = int(settings.PLUGINS_CONFIG["nautobot_lunch"]["cache_time"])
        context = cache.get_or_set(
            f"nautobot_lunch-{instance.name}-{query}", get_lunch_context(query, location=instance), cache_time
        )
        context["active_tab"] = "nautobot_lunch:1"
        return context
