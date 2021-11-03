from rest_framework import serializers
from netbox.api.serializers import PrimaryModelSerializer, WritableNestedSerializer
from netbox_dns.models import Record, Zone, NameServer


class NameServerSerializer(PrimaryModelSerializer):
    class Meta:
        model = NameServer
        fields = (
            "id",
            "display",
            "name",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
        )


class NestedNameServerSerializer(WritableNestedSerializer):
    class Meta:
        model = NameServer
        fields = (
            "id",
            "display",
            "name",
            "custom_field_data",
            "created",
            "last_updated",
        )


class RecordSerializer(PrimaryModelSerializer):
    class Meta:
        model = Record
        fields = (
            "id",
            "zone",
            "display",
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
    nameservers = NestedNameServerSerializer(
        many=True, read_only=False, required=False, help_text="Nameservers for the zone"
    )

    class Meta:
        model = Zone
        fields = (
            "id",
            "name",
            "display",
            "status",
            "nameservers",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
            "default_ttl",
        )
