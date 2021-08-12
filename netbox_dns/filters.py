import django_filters
from django.db.models import Q
from extras.filters import TagFilter
from netbox.filtersets import PrimaryModelFilterSet
from .models import NameServer, Record, Zone


class ZoneFilter(PrimaryModelFilterSet):
    """Filter capabilities for Zone instances."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    django_filters.ChoiceFilter(choices=Zone.CHOICES)

    name = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    tag = TagFilter()

    class Meta:
        model = Zone

        fields = ["name", "status", "nameservers", "tag"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(status__icontains=value)
        return queryset.filter(qs_filter)


class NameServerFilter(PrimaryModelFilterSet):
    """Filter capabilities for NameServer instances."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    name = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    tag = TagFilter()

    class Meta:
        model = NameServer

        fields = ["name", "tag"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)


class RecordFilter(PrimaryModelFilterSet):
    """Filter capabilities for Record instances."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    name = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    tag = TagFilter()

    class Meta:
        model = Record

        fields = ["name", "value", "ttl", "tag"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
