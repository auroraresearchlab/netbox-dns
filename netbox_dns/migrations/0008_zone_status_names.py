# Generated by Django 3.2.9 on 2021-11-26 07:01

from django.db import migrations
from netbox_dns.models import Zone, Record


def rename_passive_status_to_parked(apps, schema_editor):
    Zone = apps.get_model("netbox_dns", "Zone")

    for zone in Zone.objects.filter(status="passive"):
        zone.update(status=Zone.STATUS_PARKED)


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_dns", "0005_update_ns_records"),
    ]

    operations = [
        migrations.RunPython(rename_passive_status_to_parked),
    ]