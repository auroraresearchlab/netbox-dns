from utilities.testing import create_tags
from utilities.testing import ViewTestCases

from netbox_dns.models import NameServer, Zone
from netbox_dns.core.test import ModelViewTestCase


class ZoneTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
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


class NameServerTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
):
    model = NameServer

    @classmethod
    def setUpTestData(cls):
        NameServer.objects.bulk_create(
            [
                NameServer(name="Name Server 1"),
                NameServer(name="Name Server 2"),
                NameServer(name="Name Server 3"),
            ]
        )

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "Name1",
            "tags": [t.pk for t in tags],
        }

    maxDiff = None
