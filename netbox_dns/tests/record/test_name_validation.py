from django.test import TestCase
from django.core.exceptions import ValidationError

from netbox_dns.models import NameServer, Zone, Record


class NameValidationTest(TestCase):
    zone_data = {
        "default_ttl": 86400,
        "soa_rname": "hostmaster.example.com",
        "soa_refresh": 172800,
        "soa_retry": 7200,
        "soa_expire": 2592000,
        "soa_ttl": 86400,
        "soa_minimum": 3600,
        "soa_serial": 1,
        "soa_serial_auto": False,
    }

    record_data = {
        "type": "AAAA",
        "value": "fe80:dead:beef::",
    }

    @classmethod
    def setUpTestData(cls):

        cls.nameserver = NameServer.objects.create(name="ns1.example.com")

        cls.zones = (
            Zone(**cls.zone_data, soa_mname=cls.nameserver, name="zone1.example.com"),
            Zone(**cls.zone_data, soa_mname=cls.nameserver, name="zone2.example.com."),
            Zone(
                **cls.zone_data,
                soa_mname=cls.nameserver,
                name="zone240" + 22 * ".123456789" + ".example.com",
            ),
            Zone(
                **cls.zone_data,
                soa_mname=cls.nameserver,
                name="zone240" + 22 * ".987654321" + ".example.com.",
            ),
        )
        Zone.objects.bulk_create(cls.zones)

    def test_name_validation_ok(self):
        records = (
            {"name": "name1", "zone": self.zones[0]},
            {"name": "name1.zone1.example.com.", "zone": self.zones[0]},
            {"name": "name1", "zone": self.zones[1]},
            {"name": "name1.zone2.example.com.", "zone": self.zones[1]},
            {"name": "x" * 13, "zone": self.zones[2]},
            {"name": "x" * 13, "zone": self.zones[3]},
            {"name": "\\000" * 13, "zone": self.zones[2]},
            {"name": "\\000" * 13, "zone": self.zones[3]},
            {"name": "x" * 63 + f".{self.zones[0].name}.", "zone": self.zones[0]},
            {"name": "x" * 63 + f".{self.zones[1].name}", "zone": self.zones[1]},
        )

        for record in records:
            record_object = Record.objects.create(
                name=record.get("name"), zone=record.get("zone"), **self.record_data
            )
            self.assertEqual(record_object.name, record.get("name"))

    def test_name_validation_failure(self):
        records = (
            {"name": "name1..", "zone": self.zones[0]},
            {"name": "name1.zone2.example.com.", "zone": self.zones[0]},
            {"name": "name1.zone1.example.com.", "zone": self.zones[1]},
            {"name": "x" * 14, "zone": self.zones[2]},
            {"name": "x" * 14, "zone": self.zones[3]},
            {"name": "\\000" * 14, "zone": self.zones[2]},
            {"name": "\\000" * 14, "zone": self.zones[3]},
            {"name": "x" * 64 + f".{self.zones[0].name}.", "zone": self.zones[0]},
            {"name": "x" * 64 + f".{self.zones[1].name}", "zone": self.zones[1]},
        )

        for record in records:
            with self.assertRaises(ValidationError):
                Record.objects.create(
                    name=record.get("name"), zone=record.get("zone"), **self.record_data
                )
