from django.urls import reverse

from netbox.views import generic
from utilities.views import ViewTab, register_model_view

from netbox_dns.filters import ZoneFilter, RecordFilter
from netbox_dns.forms import (
    ZoneImportForm,
    ZoneForm,
    ZoneFilterForm,
    ZoneBulkEditForm,
)
from netbox_dns.models import Record, Zone
from netbox_dns.tables import (
    ZoneTable,
    RecordTable,
    ManagedRecordTable,
)


class ZoneListView(generic.ObjectListView):
    """View for listing all existing Zones."""

    queryset = Zone.objects.all().prefetch_related("view", "tags")
    filterset = ZoneFilter
    filterset_form = ZoneFilterForm
    table = ZoneTable


class ZoneView(generic.ObjectView):
    """Display Zone details"""

    queryset = Zone.objects.all().prefetch_related(
        "view",
        "tags",
        "nameservers",
        "soa_mname",
        "record_set",
    )

    def get_extra_context(self, request, instance):
        ns_warnings, ns_errors = instance.check_nameservers()

        return {
            "nameserver_warnings": ns_warnings,
            "nameserver_errors": ns_errors,
        }


class ZoneEditView(generic.ObjectEditView):
    """View for editing and creating a Zone instance."""

    queryset = Zone.objects.all().prefetch_related(
        "view", "tags", "nameservers", "soa_mname"
    )
    form = ZoneForm
    default_return_url = "plugins:netbox_dns:zone_list"


class ZoneDeleteView(generic.ObjectDeleteView):
    """View for deleting a Zone instance"""

    queryset = Zone.objects.all()
    default_return_url = "plugins:netbox_dns:zone_list"


class ZoneBulkImportView(generic.BulkImportView):
    queryset = Zone.objects.all().prefetch_related(
        "view", "tags", "nameservers", "soa_mname"
    )
    model_form = ZoneImportForm
    table = ZoneTable
    default_return_url = "plugins:netbox_dns:zone_list"


class ZoneBulkEditView(generic.BulkEditView):
    queryset = Zone.objects.all().prefetch_related(
        "view", "tags", "nameservers", "soa_mname"
    )
    filterset = ZoneFilter
    table = ZoneTable
    form = ZoneBulkEditForm
    default_return_url = "plugins:netbox_dns:zone_list"


class ZoneBulkDeleteView(generic.BulkDeleteView):
    queryset = Zone.objects.all()
    table = ZoneTable


@register_model_view(Zone, "records")
class ZoneRecordListView(generic.ObjectChildrenView):
    queryset = Zone.objects.all()
    child_model = Record
    table = RecordTable
    filterset = RecordFilter
    template_name = "netbox_dns/zone/record.html"
    hide_if_empty = True

    tab = ViewTab(
        label="Records",
        permission="netbox_dns.view_record",
        badge=lambda obj: obj.record_count(managed=False),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return Record.objects.restrict(request.user, "view").filter(
            zone=parent, managed=False
        )


@register_model_view(Zone, "managed_records")
class ZoneManagedRecordListView(generic.ObjectChildrenView):
    queryset = Zone.objects.all()
    child_model = Record
    table = ManagedRecordTable
    filterset = RecordFilter
    template_name = "netbox_dns/zone/managed_record.html"
    actions = ("changelog",)

    tab = ViewTab(
        label="Managed Records",
        permission="netbox_dns.view_record",
        badge=lambda obj: obj.record_count(managed=True),
        hide_if_empty=True,
    )

    def get_children(self, request, parent):
        return Record.objects.restrict(request.user, "view").filter(
            zone=parent, managed=True
        )
