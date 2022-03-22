from django.db import migrations
from netbox_dns.models import Record, RecordTypeChoices


def absolute_name(name):
    if name.endswith("."):
        return name
    return f"{name}."


def update_soa_record(zone):
    soa_name = "@"
    soa_ttl = zone.soa_ttl
    soa_value = (
        f"({absolute_name(zone.soa_mname.name)} {absolute_name(zone.soa_rname)}"
        f" {zone.soa_serial}"
        f" {zone.soa_refresh} {zone.soa_retry} {zone.soa_expire}"
        f" {zone.soa_minimum})"
    )

    old_soa_records = zone.record_set.filter(type=RecordTypeChoices.SOA, name=soa_name)

    if len(old_soa_records):
        for index, record in enumerate(old_soa_records):
            if index > 0:
                record.delete()
                continue

            if record.ttl != soa_ttl or record.value != soa_value:
                record.ttl = soa_ttl
                record.value = soa_value
                record.managed = True
                record.save()
    else:
        Record.objects.create(
            zone_id=zone.pk,
            type=RecordTypeChoices.SOA,
            name=soa_name,
            ttl=soa_ttl,
            value=soa_value,
            managed=True,
        )


def update_soa_records(apps, schema_editor):
    Zone = apps.get_model("netbox_dns", "Zone")

    for zone in Zone.objects.all():
        update_soa_record(zone)


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_dns", "0009_netbox32"),
    ]
    operations = [
        migrations.RunPython(update_soa_records),
    ]
