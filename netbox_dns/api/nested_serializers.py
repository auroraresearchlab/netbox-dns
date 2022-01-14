from rest_framework import serializers

from netbox.api import WritableNestedSerializer
from netbox_dns import models


#
# Nameservers
#


class NestedNameServerSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:nameserver-detail"
    )

    class Meta:
        model = models.NameServer
        fields = ["id", "url", "display", "name"]


#
# Zones
#


class NestedZoneSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:zone-detail"
    )
    active = serializers.BooleanField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = models.Zone
        fields = ["id", "url", "display", "name", "status", "active"]


#
# Records
#


class NestedRecordSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:record-detail"
    )
    zone = NestedZoneSerializer(
        many=False,
        required=False,
        help_text="Zone the record belongs to",
    )
    active = serializers.BooleanField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = models.Record
        fields = [
            "id",
            "url",
            "display",
            "type",
            "name",
            "value",
            "ttl",
            "zone",
            "active",
        ]
