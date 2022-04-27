from utilities.testing import ViewTestCases
from utilities.testing import create_tags

from netbox_dns.tests.custom import ModelViewTestCase
from netbox_dns.models import View, Zone, NameServer, Record, RecordTypeChoices


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

    zone_data = {
        "default_ttl": 86400,
        "soa_rname": "hostmaster.example.com",
        "soa_serial": 2021110401,
        "soa_refresh": 172800,
        "soa_retry": 7200,
        "soa_expire": 2592000,
        "soa_ttl": 86400,
        "soa_minimum": 3600,
        "soa_serial_auto": False,
    }

    csv_data = (
        "zone,view,type,name,value,ttl",
        "zone1.example.com,,A,@,10.10.10.10,3600",
        "zone2.example.com,,AAAA,name4,fe80::dead:beef,7200",
        "zone1.example.com,,CNAME,dns,name1.zone2.example.com,100",
        "zone2.example.com,,TXT,textname,textvalue,1000",
        "zone1.example.com,view1,A,@,10.10.10.10,3600",
        "zone2.example.com,view1,AAAA,name4,fe80::dead:beef,7200",
        "zone1.example.com,view1,CNAME,dns,name1.zone2.example.com,100",
        "zone2.example.com,view1,TXT,textname,textvalue,1000",
        "zone1.example.com,view2,A,@,10.10.10.10,3600",
        "zone2.example.com,view2,AAAA,name4,fe80::dead:beef,7200",
        "zone1.example.com,view2,CNAME,dns,name1.zone2.example.com,100",
        "zone2.example.com,view2,TXT,textname,textvalue,1000",
    )

    @classmethod
    def setUpTestData(cls):
        ns1 = NameServer.objects.create(name="ns1.example.com")

        views = (
            View(name="view1"),
            View(name="view2"),
        )
        View.objects.bulk_create(views)

        zones = (
            Zone(name="zone1.example.com", **cls.zone_data, soa_mname=ns1, view=None),
            Zone(name="zone2.example.com", **cls.zone_data, soa_mname=ns1, view=None),
            Zone(
                name="zone1.example.com", **cls.zone_data, soa_mname=ns1, view=views[0]
            ),
            Zone(
                name="zone2.example.com", **cls.zone_data, soa_mname=ns1, view=views[0]
            ),
            Zone(
                name="zone1.example.com", **cls.zone_data, soa_mname=ns1, view=views[1]
            ),
            Zone(
                name="zone2.example.com", **cls.zone_data, soa_mname=ns1, view=views[1]
            ),
        )
        Zone.objects.bulk_create(zones)

        records = (
            Record(
                zone=zones[0],
                type=RecordTypeChoices.CNAME,
                name="name1",
                value="test1.example.com",
                ttl=100,
            ),
            Record(
                zone=zones[1],
                type=RecordTypeChoices.A,
                name="name2",
                value="192.168.1.1",
                ttl=200,
            ),
        )
        Record.objects.bulk_create(records)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "zone": zones[0].pk,
            "type": RecordTypeChoices.AAAA,
            "name": "name3",
            "value": "fe80::dead:beef",
            "ttl": 300,
            "tags": [t.pk for t in tags],
        }

        cls.bulk_edit_data = {
            "zone": zones[1].pk,
            "ttl": 999,
        }

    maxDiff = None
