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

        cls.csv_data = (
            "name,status",
            "domain-4.com,active",
            "domain-5.com,active",
            "domain-6.com,active",
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

        cls.csv_data = (
            "name",
            "name-server-4.com",
            "name-server-5.com",
            "name-server-6.com",
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
        zone1 = Zone.objects.create(name="zone1.com")
        zone2 = Zone.objects.create(name="zone2.com")

        records = [
            Record(
                zone=zone1,
                type=Record.CNAME,
                name="name 1",
                value="value 1",
                ttl=100,
            ),
            Record(
                zone=zone2,
                type=Record.A,
                name="name 2",
                value="value 2",
                ttl=200,
            ),
        ]

        Record.objects.bulk_create(records)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "zone": zone1.id,
            "type": Record.AAAA,
            "name": "name 3",
            "value": "value 300",
            "ttl": 300,
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "zone,type,name,value,ttl",
            "zone1.com,A,@,10.10.10.10,3600",
            "zone2.com,AAAA,ipv6sub,[00:00],7200",
            "zone1.com,CNAME,dns,100.100.100.100,100",
            "zone2.com,TXT,textname,textvalue,1000",
        )

        cls.bulk_edit_data = {
            "zone": zone2.id,
            "ttl": 999,
        }

    maxDiff = None
