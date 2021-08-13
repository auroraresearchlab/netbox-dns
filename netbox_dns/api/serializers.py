from rest_framework import serializers
from netbox.api.serializers import PrimaryModelSerializer
from netbox_dns.models import Record, Zone, NameServer


class NameServerSerializer(PrimaryModelSerializer):
    class Meta:
        model = NameServer
        fields = ("id", "name", "tags", "custom_field_data", "created", "last_updated")


class RecordSerializer(PrimaryModelSerializer):
    class Meta:
        model = Record
        fields = (
            "id",
            "zone",
            "type",
            "name",
            "value",
            "ttl",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
        )


class ZoneSerializer(PrimaryModelSerializer):
    class Meta:
        model = Zone
        fields = (
            "id",
            "name",
            "status",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
        )
