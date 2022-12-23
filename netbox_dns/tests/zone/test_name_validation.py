from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError

from netbox_dns.models import NameServer, Zone


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

    @classmethod
    def setUpTestData(cls):

        cls.nameserver = NameServer.objects.create(name="ns1.example.com")

    def test_name_validation_ok(self):
        names = (
            "zone1.example.com",
            "zone2.example.com.",
            "zone-1.example.com",  # dash in first label
            "zone1.example-1.com",  # dash in second label
            "1234567" + ".12345678" * 26 + ".example.com",  # 254 octets
            "1234567" + ".12345678" * 26 + ".example.com.",  # 255 octets, trailing dot
            "x" * 63 + ".example.com",  # longest label 63 octets
            "x" * 63 + ".example.com.",  # longest label 63 octets, trailing dot
        )

        for name in names:
            zone = Zone.objects.create(
                name=name, **self.zone_data, soa_mname=self.nameserver
            )
            self.assertEqual(zone.name, name)

    def test_name_validation_failure(self):
        names = (
            "-zone.example.com",  # leading dash in first label
            "zone1.-example.com",  # leading dash in second label
            "zone1.example.com-1",  # dash in TLD
            "zone1..example.com",  # empty label
            "-zone1..example.com-1",  # leading dash
            "x" * 64 + ".example.com",  # label too long
            "12345678" + ".12345678" * 26 + ".example.com",  # 255 octets
            "123456789"
            + ".12345678" * 26
            + ".example.com.",  # 256 octets, trailing dot
        )

        for name in names:
            with self.assertRaises(ValidationError):
                Zone.objects.create(
                    name=name, **self.zone_data, soa_mname=self.nameserver
                )

    @override_settings(
        PLUGINS_CONFIG={"netbox_dns": {"tolerate_underscores_in_hostnames": True}}
    )
    def test_name_validation_tolerant_ok(self):
        names = (
            "zone_1.example.com",  # underscore in first label
            "zone1.example_1.com",  # underscore in second label
        )

        for name in names:
            zone = Zone.objects.create(
                name=name, **self.zone_data, soa_mname=self.nameserver
            )
            self.assertEqual(zone.name, name)

    @override_settings(
        PLUGINS_CONFIG={"netbox_dns": {"tolerate_underscores_in_hostnames": True}}
    )
    def test_name_validation_tolerant_failure(self):
        names = (
            "_zone1.example.com",  # leading underscore in first label
            "zone1._example.com",  # leading underscore in second label
            "zone1.example.com_1",  # underscore in TLD
            "zone1..example.com",  # empty label
            "x" * 64 + ".example.com",  # label too long
            "12345678" + ".12345678" * 26 + ".example.com",  # 255 octets
            "123456789" + ".12345678" * 26 + ".example.com",  # 256 octets, trailing dot
        )

        for name in names:
            with self.assertRaises(ValidationError):
                Zone.objects.create(
                    name=name, **self.zone_data, soa_mname=self.nameserver
                )
