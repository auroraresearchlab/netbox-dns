from utilities.testing import APIViewTestCases

from netbox_dns.tests.custom import APITestCase
from netbox_dns.models import NameServer, Zone


class ZoneTest(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = Zone

    brief_fields = [
        "active",
        "display",
        "id",
        "name",
        "status",
        "url",
    ]

    bulk_update_data = {
        "status": "active",
    }

    zone_data = {
        "default_ttl": 86400,
        "soa_rname": "hostmaster.example.com",
        "soa_refresh": 172800,
        "soa_retry": 7200,
        "soa_expire": 2592000,
        "soa_ttl": 86400,
        "soa_minimum": 3600,
        "soa_serial_auto": False,
    }

    @classmethod
    def setUpTestData(cls):
        ns1 = NameServer.objects.create(name="ns1.example.com")

        zones = (
            Zone(name="zone1.example.com", **cls.zone_data, soa_mname=ns1),
            Zone(name="zone2.example.com", **cls.zone_data, soa_mname=ns1),
            Zone(name="zone3.example.com", **cls.zone_data, soa_mname=ns1),
        )
        Zone.objects.bulk_create(zones)

        cls.create_data = [
            {
                "name": "zone4.example.com",
                "status": "reserved",
                **cls.zone_data,
                "soa_mname": ns1.pk,
            },
            {
                "name": "zone5.example.com",
                "status": "reserved",
                **cls.zone_data,
                "soa_mname": ns1.pk,
            },
            {
                "name": "zone6.example.com",
                "status": "reserved",
                **cls.zone_data,
                "soa_mname": ns1.pk,
            },
        ]
