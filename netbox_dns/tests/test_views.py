from utilities.testing import create_tags
from utilities.testing import ViewTestCases

from netbox_dns.models import Zone
from netbox_dns.core.test import ModelViewTestCase


class ZoneTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    # ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
):
    model = Zone

    @classmethod
    def setUpTestData(cls):
        Zone.objects.bulk_create(
            [
                Zone(name="Zone 1"),
                Zone(name="Zone 2"),
                Zone(name="Zone 3"),
            ]
        )

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Name1",
            "tags": [t.pk for t in tags],
        }

    maxDiff = None
