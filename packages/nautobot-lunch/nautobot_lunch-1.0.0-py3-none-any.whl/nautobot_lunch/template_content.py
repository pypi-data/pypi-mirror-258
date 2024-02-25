"""Nautobot Lunch template content."""

from django.urls import reverse

from nautobot.apps.ui import TemplateExtension


class LocationContent(TemplateExtension):  # pylint: disable=abstract-method
    """Extend Locations to provide lunch."""

    model = "dcim.location"

    def detail_tabs(self):
        """Return Lunch Detail Tab if the Location has a physical address or latitude and longitude."""
        if (
            self.context["object"].physical_address != ""
            or self.context["object"].latitude is not None
            and self.context["object"].longitude is not None
        ):
            return [
                {
                    "title": "🍴 Find Lunch",
                    "url": reverse(
                        "plugins:nautobot_lunch:location_detail_lunch", kwargs={"pk": self.context["object"].pk}
                    ),
                },
            ]
        return []


template_extensions = [LocationContent]
