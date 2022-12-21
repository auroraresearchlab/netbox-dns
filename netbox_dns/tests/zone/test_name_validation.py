from django.test import TestCase
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
            "ns1..example.com",  # empty label
            "x" * 64 + ".example.com",  # label too long
            "12345678" + ".12345678" * 26 + ".example.com",  # 255 octets
            "123456789" + ".12345678" * 26 + ".example.com",  # 256 octets, trailing dot
        )

        for name in names:
            with self.assertRaises(ValidationError):
                Zone.objects.create(
                    name=name, **self.zone_data, soa_mname=self.nameserver
                )
