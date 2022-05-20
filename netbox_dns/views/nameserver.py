from netbox.views import generic

from netbox_dns.filters import NameServerFilter
from netbox_dns.forms import (
    NameServerCSVForm,
    NameServerFilterForm,
    NameServerForm,
    NameServerBulkEditForm,
)
from netbox_dns.models import Zone, NameServer
from netbox_dns.tables import NameServerTable, ZoneTable


class NameServerListView(generic.ObjectListView):
    queryset = NameServer.objects.all()
    filterset = NameServerFilter
    filterset_form = NameServerFilterForm
    table = NameServerTable


class NameServerView(generic.ObjectView):
    """Display NameServer details"""

    queryset = NameServer.objects.all().prefetch_related("zones")

    def get_extra_context(self, request, instance):
        zones = instance.zones.all()
        zone_table = ZoneTable(list(zones), user=request.user)

        change_zone = request.user.has_perm("netbox_dns.change_zone")
        delete_zone = request.user.has_perm("netbox_dns.delete_zone")

        if change_zone or delete_zone:
            zone_table.columns.show("pk")
        zone_table.configure(request)

        return {
            "zone_table": zone_table,
            "permissions": {
                "change": change_zone,
                "delete": delete_zone,
            },
            "model": Zone,
        }


class NameServerEditView(generic.ObjectEditView):
    """View for editing a Name Server instance."""

    queryset = NameServer.objects.all()
    form = NameServerForm


class NameServerDeleteView(generic.ObjectDeleteView):
    queryset = NameServer.objects.all()
    default_return_url = "plugins:netbox_dns:nameserver_list"


class NameServerBulkImportView(generic.BulkImportView):
    queryset = NameServer.objects.all()
    model_form = NameServerCSVForm
    table = NameServerTable


class NameServerBulkEditView(generic.BulkEditView):
    queryset = NameServer.objects.all()
    filterset = NameServerFilter
    table = NameServerTable
    form = NameServerBulkEditForm


class NameServerBulkDeleteView(generic.BulkDeleteView):
    queryset = NameServer.objects.all()
    table = NameServerTable
