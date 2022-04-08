from netbox.views import generic

from netbox_dns.filters import RecordFilter, ZoneFilter
from netbox_dns.forms import (
    RecordFilterForm,
    ZoneCSVForm,
    ZoneForm,
    ZoneFilterForm,
    ZoneBulkEditForm,
)
from netbox_dns.models import Record, Zone
from netbox_dns.tables import (
    ZoneTable,
    ZoneManagedRecordTable,
    ZoneRecordTable,
)


class ZoneListView(generic.ObjectListView):
    """View for listing all existing Zones."""

    queryset = Zone.objects.all()
    filterset = ZoneFilter
    filterset_form = ZoneFilterForm
    table = ZoneTable


class ZoneView(generic.ObjectView):
    """Display Zone details"""

    queryset = Zone.objects.all()

    def get_extra_context(self, request, instance):
        ns_warnings, ns_errors = instance.check_nameservers()

        return {
            "nameserver_warnings": ns_warnings,
            "nameserver_errors": ns_errors,
        }


class ZoneEditView(generic.ObjectEditView):
    """View for editing and creating a Zone instance."""

    queryset = Zone.objects.all()
    form = ZoneForm


class ZoneDeleteView(generic.ObjectDeleteView):
    """View for deleting a Zone instance"""

    queryset = Zone.objects.all()


class ZoneBulkImportView(generic.BulkImportView):
    queryset = Zone.objects.all()
    model_form = ZoneCSVForm
    table = ZoneTable


class ZoneBulkEditView(generic.BulkEditView):
    queryset = Zone.objects.all()
    filterset = ZoneFilter
    table = ZoneTable
    form = ZoneBulkEditForm


class ZoneBulkDeleteView(generic.BulkDeleteView):
    queryset = Zone.objects.all()
    table = ZoneTable


class ZoneRecordListView(generic.ObjectView):
    queryset = Zone.objects.all()
    template_name = "netbox_dns/zone_record.html"

    def get_extra_context(self, request, instance):
        zone_records = Record.objects.filter(managed=False, zone_id=instance.pk)

        table = ZoneRecordTable(list(zone_records), user=request.user)
        if request.user.has_perm("netbox_dns.change_record") or request.user.has_perm(
            "netbox_dns.delete_record"
        ):
            table.columns.show("pk")
        table.configure(request)

        permissions = {
            "change": request.user.has_perm("netbox_dns.change_record"),
            "delete": request.user.has_perm("netbox_dns.delete_record"),
        }
        bulk_querystring = f"zone_id={instance.pk}"

        return {
            "active_tab": "record_list",
            "table": table,
            "permissions": permissions,
            "bulk_querystring": bulk_querystring,
        }


class ZoneManagedRecordListView(generic.ObjectView):
    queryset = Zone.objects.all()
    template_name = "netbox_dns/zone_managed_record.html"

    def get_extra_context(self, request, instance):
        zone_records = Record.objects.filter(managed=True, zone_id=instance.pk)

        table = ZoneManagedRecordTable(list(zone_records), user=request.user)
        table.configure(request)

        return {
            "active_tab": "managed_record_list",
            "table": table,
        }
