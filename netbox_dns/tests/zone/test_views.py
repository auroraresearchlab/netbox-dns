from utilities.testing import ViewTestCases
from utilities.testing import create_tags

from netbox_dns.tests.custom import ModelViewTestCase
from netbox_dns.models import Zone, NameServer


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

    csv_data = (
        f"name,status,soa_mname,soa_rname",
        f"zone4.example.com,active,ns1.example.com,hostmaster.example.com",
        f"zone5.example.com,active,ns1.example.com,hostmaster.example.com",
        f"zone6.example.com,active,ns1.example.com,hostmaster.example.com",
    )

    bulk_edit_data = {
        "status": Zone.STATUS_PARKED,
    }

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
    zone_value_string = ",".join(str(value) for value in zone_data.values())
    zone_key_string = ",".join(zone_data.keys())

    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        ns1 = NameServer.objects.create(name="ns1.example.com")

        zones = (
            Zone(name="zone1.example.com", **cls.zone_data, soa_mname=ns1),
            Zone(name="zone2.example.com", **cls.zone_data, soa_mname=ns1),
            Zone(name="zone3.example.com", **cls.zone_data, soa_mname=ns1),
        )
        Zone.objects.bulk_create(zones)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "zone4.example.com",
            "default_ttl": 7200,
            "tags": [t.pk for t in tags],
        }

        cls.form_data = {
            "name": "zone7.example.com",
            "status": "parked",
            **cls.zone_data,
            "soa_mname": ns1.pk,
        }
