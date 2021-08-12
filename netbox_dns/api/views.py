from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from netbox_dns.models import Zone, NameServer, Record
from netbox_dns.api.serializers import (
    ZoneSerializer,
    NameServerSerializer,
    RecordSerializer,
)
from netbox_dns.filters import ZoneFilter, NameServerFilter, RecordFilter


class ZoneViewSet(ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filterset_class = ZoneFilter

    @action(detail=True, methods=["get"])
    def records(self, request, pk=None):
        records = Record.objects.filter(zone=pk)
        serializer = RecordSerializer(records, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def nameservers(self, request, pk=None):
        nameservers = NameServer.objects.filter(zones__id=pk)
        serializer = NameServerSerializer(
            nameservers, many=True, context={"request": request}
        )
        return Response(serializer.data)


class NameServerViewSet(ModelViewSet):
    queryset = NameServer.objects.all()
    serializer_class = NameServerSerializer
    filterset_class = NameServerFilter


class RecordViewSet(ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    filterset_class = RecordFilter
