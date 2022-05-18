from netbox.views import generic

from netbox_dns.models import View, Zone
from netbox_dns.filters import ViewFilter
from netbox_dns.forms import ViewForm, ViewFilterForm, ViewCSVForm, ViewBulkEditForm
from netbox_dns.tables import ViewTable, ZoneTable


class ViewView(generic.ObjectView):
    queryset = View.objects.all().prefetch_related("zone_set")

    def get_extra_context(self, request, instance):
        zones = instance.zone_set.all()
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


class ViewListView(generic.ObjectListView):
    queryset = View.objects.all()
    table = ViewTable
    filterset = ViewFilter
    filterset_form = ViewFilterForm


class ViewEditView(generic.ObjectEditView):
    queryset = View.objects.all()
    form = ViewForm


class ViewDeleteView(generic.ObjectDeleteView):
    queryset = View.objects.all()
    default_return_url = "plugins:netbox_dns:view_list"


class ViewBulkImportView(generic.BulkImportView):
    queryset = View.objects.all()
    model_form = ViewCSVForm
    table = ViewTable


class ViewBulkEditView(generic.BulkEditView):
    queryset = View.objects.all()
    filterset = ViewFilter
    table = ViewTable
    form = ViewBulkEditForm


class ViewBulkDeleteView(generic.BulkDeleteView):
    queryset = View.objects.all()
    table = ViewTable
