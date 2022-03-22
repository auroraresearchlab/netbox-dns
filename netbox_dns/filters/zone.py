import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_dns.models import Zone, ZoneStatusChoices


class ZoneFilter(NetBoxModelFilterSet):
    """Filter capabilities for Zone instances."""

    status = django_filters.ChoiceFilter(
        choices=ZoneStatusChoices,
    )

    class Meta:
        model = Zone
        fields = ("name", "status", "nameservers")

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(status__icontains=value)
        return queryset.filter(qs_filter)
