import sys

from packaging import version

from django.core import management
from django.db import migrations
from django.conf import settings


def reindex(apps, schema_editor):
    if "test" not in sys.argv:
        if version.parse(settings.VERSION) >= version.parse("3.4.2"):
            management.call_command("reindex", "netbox_dns")
        else:
            management.call_command("reindex", "netbox_dns.view")
            management.call_command("reindex", "netbox_dns.nameserver")
            management.call_command("reindex", "netbox_dns.zone")
            management.call_command("reindex", "netbox_dns.record")


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0083_search"),
        ("netbox_dns", "0021_record_ip_address"),
    ]

    operations = [
        migrations.RunPython(code=reindex, reverse_code=migrations.RunPython.noop),
    ]
