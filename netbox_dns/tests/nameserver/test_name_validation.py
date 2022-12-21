from django.test import TestCase
from django.core.exceptions import ValidationError

from netbox_dns.models import NameServer


class NameValidationTest(TestCase):
    def test_name_validation_ok(self):
        names = (
            "ns1.example.com",
            "ns2.example.com.",
            "1234567" + ".12345678" * 26 + ".example.com",  # 254 octets
            "1234567" + ".12345678" * 26 + ".example.com.",  # 255 octets, trailing dot
            "x" * 63 + ".example.com",  # longest label 63 octets
            "x" * 63 + ".example.com.",  # longest label 63 octets, trailing dot
        )

        for name in names:
            nameserver = NameServer.objects.create(name=name)
            self.assertEqual(nameserver.name, name)

    def test_name_validation_failure(self):
        names = (
            "ns1..example.com",  # empty label
            "x" * 64 + ".example.com",  # label too long
            "12345678" + ".12345678" * 26 + ".example.com",  # 255 octets
            "123456789" + ".12345678" * 26 + ".example.com",  # 256 octets, trailing dot
        )

        for name in names:
            with self.assertRaises(ValidationError):
                NameServer.objects.create(name=name)
