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
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Zone

    @classmethod
    def setUpTestData(cls):
        Zone.objects.bulk_create(
            [
                Zone(name="zone1.example.com", default_ttl="86400"),
                Zone(name="zone2.example.com", default_ttl="43200"),
                Zone(name="zone3.example.com", default_ttl="21600"),
            ]
        )

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "zone4.example.com",
            "default_ttl": 7200,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,status,default_ttl",
            "zone5.example.com,active,86400",
            "zone6.example.com,active,86400",
            "zone7.example.com,active,86400",
        )

        cls.bulk_edit_data = {
            "status": Zone.STATUS_PASSIVE,
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
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = NameServer

    @classmethod
    def setUpTestData(cls):
        NameServer.objects.bulk_create(
            [
                NameServer(name="ns1.example.com"),
                NameServer(name="ns2.example.com"),
                NameServer(name="ns3.example.com"),
            ]
        )

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "ns4.example.com",
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name",
            "ns5.example.com",
            "ns6.example.com",
            "ns7.example.com",
        )

    maxDiff = None


class RecordTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkEditObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = Record

    @classmethod
    def setUpTestData(cls):
        zone1 = Zone.objects.create(name="zone1.example.com", default_ttl="86400")
        zone2 = Zone.objects.create(name="zone2.example.com", default_ttl="86400")

        records = [
            Record(
                zone=zone1,
                type=Record.CNAME,
                name="name1",
                value="test1.example.com",
                ttl=100,
            ),
            Record(
                zone=zone2,
                type=Record.A,
                name="name2",
                value="192.168.1.1",
                ttl=200,
            ),
        ]

        Record.objects.bulk_create(records)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "zone": zone1.id,
            "type": Record.AAAA,
            "name": "name3",
            "value": "fe80::dead:beef",
            "ttl": 300,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "zone,type,name,value,ttl",
            "zone1.example.com,A,@,10.10.10.10,3600",
            "zone2.example.com,AAAA,name4,[fe80::dead:beef],7200",
            "zone1.example.com,CNAME,dns,name1.zone2.example.com,100",
            "zone2.example.com,TXT,textname,textvalue,1000",
        )

        cls.bulk_edit_data = {
            "zone": zone2.id,
            "ttl": 999,
        }

    maxDiff = None
