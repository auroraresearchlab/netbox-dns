from django.urls import reverse
from utilities.testing import APIViewTestCases
from netbox_dns.models import NameServer, Record, Zone
from netbox_dns.core.test import APITestCase


class AppTest(APITestCase):
    def test_root(self):

        url = reverse("plugins-api:netbox_dns-api:api-root")
        response = self.client.get("{}?format=api".format(url), **self.header)

        self.assertEqual(response.status_code, 200)


class ZoneTest(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = Zone
    brief_fields = ["display", "id", "name", "status", "url"]
    create_data = [
        {"name": "zone1.com", "status": "passive"},
        {"name": "zone2.com", "status": "passive"},
        {"name": "zone3.com", "status": "passive"},
    ]
    bulk_update_data = {
        "status": "active",
    }

    @classmethod
    def setUpTestData(cls):
        zones = (
            Zone(name="zone4.com"),
            Zone(name="zone5.com"),
            Zone(name="zone6.com"),
        )
        Zone.objects.bulk_create(zones)


class NameServerTest(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = NameServer
    brief_fields = ["display", "id", "name", "url"]
    create_data = [
        {
            "name": "name-server-1.com",
        },
        {
            "name": "name-server-2.com",
        },
        {
            "name": "name-server-3.com",
        },
    ]

    @classmethod
    def setUpTestData(cls):
        nameservers = (
            NameServer(name="name-server-4.com"),
            NameServer(name="name-server-5.com"),
            NameServer(name="name-server-6.com"),
        )
        NameServer.objects.bulk_create(nameservers)


class RecordTest(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = Record
    brief_fields = ["display", "id", "name", "ttl", "type", "url", "value"]
    bulk_update_data = {
        "value": "value value value",
        "url": 5555,
    }

    @classmethod
    def setUpTestData(cls):
        zones = (
            Zone(name="zone-4.com"),
            Zone(name="zone-5.com"),
            Zone(name="zone-6.com"),
        )
        Zone.objects.bulk_create(zones)

        records = (
            Record(
                zone=zones[0], type=Record.A, name="name1", value="A Record", ttl=111
            ),
            Record(
                zone=zones[1],
                type=Record.AAAA,
                name="name2",
                value="AAAA Record",
                ttl=222,
            ),
            Record(
                zone=zones[2],
                type=Record.TXT,
                name="name3",
                value="TXT Record",
                ttl=333,
            ),
        )
        Record.objects.bulk_create(records)

        cls.create_data = [
            {
                "zone": zones[0].pk,
                "type": Record.A,
                "name": "name1",
                "value": "A Record",
                "ttl": 123,
            },
            {
                "zone": zones[1].pk,
                "type": Record.AAAA,
                "name": "name2",
                "value": "AAAA Record",
                "ttl": 123,
            },
            {
                "zone": zones[2].pk,
                "type": Record.TXT,
                "name": "name3",
                "value": "TXT Record",
                "ttl": 123,
            },
        ]
