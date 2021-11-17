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

    class Meta:
        model = models.Zone
        fields = ["id", "url", "display", "name", "status"]


#
# Records
#


class NestedRecordSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_dns-api:record-detail"
    )

    class Meta:
        model = models.Record
        fields = ["id", "url", "display", "type", "name", "value", "ttl"]
