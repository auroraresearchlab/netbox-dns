from django.db import migrations

from netbox_dns.models import ZoneStatusChoices


def rename_passive_status_to_parked(apps, schema_editor):
    Zone = apps.get_model("netbox_dns", "Zone")

    for zone in Zone.objects.filter(status="passive"):
        zone.status = ZoneStatusChoices.STATUS_PARKED
        zone.save()


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_dns", "0005_update_ns_records"),
    ]

    operations = [
        migrations.RunPython(rename_passive_status_to_parked),
    ]
