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
        {"name": "zone1.com", "status": "passive", "default_ttl": 86400},
        {"name": "zone2.com", "status": "passive", "default_ttl": 86400},
        {"name": "zone3.com", "status": "passive", "default_ttl": 9600},
    ]
    bulk_update_data = {
        "status": "active",
    }

    @classmethod
    def setUpTestData(cls):
        zones = (
            Zone(name="zone4.com", default_ttl=86400),
            Zone(name="zone5.com", default_ttl=86400),
            Zone(name="zone6.com", default_ttl=86400),
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
            "name": "ns1.example.com",
        },
        {
            "name": "ns2.example.com",
        },
        {
            "name": "ns3.example.com",
        },
    ]

    @classmethod
    def setUpTestData(cls):
        nameservers = (
            NameServer(name="ns4.example.com"),
            NameServer(name="ns5.example.com"),
            NameServer(name="ns6.example.com"),
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
        "value": "2.2.2.2",
        "ttl": 4800
    }

    @classmethod
    def setUpTestData(cls):
        zones = (
            Zone(name="zone.com", default_ttl=86400),
            Zone(name="zone2.com", default_ttl=9600),
            Zone(name="zone3.com", default_ttl=86400),
        )
        Zone.objects.bulk_create(zones)

        records = (
            Record(
                zone=zones[0],
                type=Record.A,
                name="example1",
                value="192.168.1.1",
                ttl=5000,
            ),
            Record(
                zone=zones[1],
                type=Record.AAAA,
                name="example2",
                value="[fe80::dead:beef]",
                ttl=6000,
            ),
            Record(
                zone=zones[2],
                type=Record.TXT,
                name="example3",
                value="TXT Record",
                ttl=7000,
            ),
        )
        Record.objects.bulk_create(records)

        cls.create_data = [
            {
                "zone": zones[0].pk,
                "type": Record.A,
                "name": "name3",
                "value": "1.1.1.1",
                "ttl": 9600,
            },
            {
                "zone": zones[1].pk,
                "type": Record.AAAA,
                "name": "name4",
                "value": "fe80::dead:beef",
                "ttl": 9600,
            },
            {
                "zone": zones[2].pk,
                "type": Record.TXT,
                "name": "name5",
                "value": "TXT Record",
                "ttl": 9600,
            },
        ]
