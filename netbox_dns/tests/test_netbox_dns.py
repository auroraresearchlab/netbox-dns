from django.urls import reverse
from django.test import SimpleTestCase

from netbox_dns import __version__
from netbox_dns.tests.custom import APITestCase


class NetboxDnsVersionTestCase(SimpleTestCase):
    """
    Test for netbox_dns package
    """

    def test_version(self):
        assert __version__ == "0.10.0"


class AppTest(APITestCase):
    """
    Test the availability of the NetBox DNS API root
    """

    def test_root(self):
        url = reverse("plugins-api:netbox_dns-api:api-root")
        response = self.client.get(f"{url}?format=api", **self.header)

        self.assertEqual(response.status_code, 200)
