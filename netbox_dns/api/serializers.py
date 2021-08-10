from netbox.api.serializers import PrimaryModelSerializer

from netbox_dns.models import Zone, NameServer


class ZoneSerializer(PrimaryModelSerializer):
    class Meta:
        model = Zone
        fields = ("id", "name", "tags", "custom_field_data", "created", "last_updated")


class NameServerSerializer(PrimaryModelSerializer):
    class Meta:
        model = NameServer
        fields = ("id", "name", "tags", "custom_field_data", "created", "last_updated")
