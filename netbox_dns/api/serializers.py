from rest_framework import serializers
from netbox.api.serializers import PrimaryModelSerializer, WritableNestedSerializer
from netbox_dns.models import Record, Zone, NameServer
from netbox_dns.api.nested_serializers import (
    NestedZoneSerializer,
    NestedRecordSerializer,
    NestedNameServerSerializer,
)


class NameServerSerializer(PrimaryModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:nameserver-detail"
    )

    class Meta:
        model = NameServer
        fields = (
            "id",
            "url",
            "display",
            "name",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
        )


class RecordSerializer(PrimaryModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:record-detail"
    )

    class Meta:
        model = Record
        fields = (
            "id",
            "url",
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
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:zone-detail"
    )
    nameservers = NestedNameServerSerializer(
        many=True, read_only=False, required=False, help_text="Nameservers for the zone"
    )

    class Meta:
        model = Zone
        fields = (
            "id",
            "url",
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
