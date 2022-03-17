import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_dns.models import NameServer


class NameServerFilter(NetBoxModelFilterSet):
    """Filter capabilities for NameServer instances."""

    name = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = NameServer
        fields = ("name",)
