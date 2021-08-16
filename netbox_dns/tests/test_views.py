from utilities.testing import create_tags
from utilities.testing import ViewTestCases

from netbox_dns.models import NameServer, Record, Zone
from netbox_dns.core.test import ModelViewTestCase


class ZoneTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
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
    ViewTestCases.GetObjectChangelogViewTestCase,
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


class RecordTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
):
    model = Record

    @classmethod
    def setUpTestData(cls):
        zone = Zone.objects.create(name="zone.com")

        Record.objects.bulk_create(
            [
                Record(
                    zone=zone,
                    type=Record.CNAME,
                    name="name 1",
                    value="value 1",
                    ttl=100,
                ),
                Record(
                    zone=zone,
                    type=Record.A,
                    name="name 2",
                    value="value 2",
                    ttl=200,
                ),
            ]
        )

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "zone": zone.id,
            "type": Record.AAAA,
            "name": "name 3",
            "value": "value 300",
            "ttl": 300,
            "tags": [t.pk for t in tags],
        }

    maxDiff = None
