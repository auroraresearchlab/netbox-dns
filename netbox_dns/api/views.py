from rest_framework.viewsets import ModelViewSet

from netbox_dns.models import Zone, NameServer
from netbox_dns.api.serializers import NameServerSerializer, ZoneSerializer
from netbox_dns.filters import NameServerFilter, ZoneFilter


class ZoneViewSet(ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filterset_class = ZoneFilter


class NameServerViewSet(ModelViewSet):
    queryset = NameServer.objects.all()
    serializer_class = NameServerSerializer
    filterset_class = NameServerFilter
