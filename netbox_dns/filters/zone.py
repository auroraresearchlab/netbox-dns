import django_filters
from django.db.models import Q

from netbox.filtersets import NetBoxModelFilterSet

from netbox_dns.models import Zone


class ZoneFilter(NetBoxModelFilterSet):
    """Filter capabilities for Zone instances."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    status = django_filters.ChoiceFilter(
        choices=Zone.CHOICES,
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
