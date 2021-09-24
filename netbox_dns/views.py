from django.shortcuts import render, get_object_or_404

from netbox.views import generic

from netbox_dns.models import Record, Zone, NameServer
from netbox_dns.tables import NameServerTable, RecordTable, ZoneTable
from netbox_dns.forms import (
    NameServerCSVForm,
    NameServerFilterForm,
    NameServerForm,
    RecordCSVForm,
    RecordFilterForm,
    RecordForm,
    RecordBulkEditForm,
    ZoneCSVForm,
    ZoneForm,
    ZoneFilterForm,
    ZoneBulkEditForm,
)
from netbox_dns.filters import NameServerFilter, RecordFilter, ZoneFilter


#
# Zone
#


class ZoneListView(generic.ObjectListView):
    """View for listing all existing Zones."""

    queryset = Zone.objects.all()
    filterset = ZoneFilter
    filterset_form = ZoneFilterForm
    table = ZoneTable
    template_name = "netbox_dns/object_list.html"
    action_buttons = ("add", "import")


class ZoneView(generic.ObjectView):
    """Display Zone details"""

    queryset = Zone.objects.all()

    def get_extra_context(self, request, instance):
        records = instance.record_set.all()
        return {"records": records}


class ZoneEditView(generic.ObjectEditView):
    """View for editing and creating a Zone instance."""

    queryset = Zone.objects.all()
    model_form = ZoneForm


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


#
# NameServer
#


class NameServerListView(generic.ObjectListView):
    queryset = NameServer.objects.all()
    filterset = NameServerFilter
    filterset_form = NameServerFilterForm
    table = NameServerTable
    template_name = "netbox_dns/object_list.html"

    action_buttons = ("add", "import")


class NameServerView(generic.ObjectView):
    """Display NameServer details"""

    queryset = NameServer.objects.all()


class NameServerEditView(generic.ObjectEditView):
    """View for editing a Name Server instance."""

    queryset = NameServer.objects.all()
    model_form = NameServerForm


class NameServerDeleteView(generic.ObjectDeleteView):
    queryset = NameServer.objects.all()


class NameServerBulkImportView(generic.BulkImportView):
    queryset = NameServer.objects.all()
    model_form = NameServerCSVForm
    table = NameServerTable


class NameServerBulkDeleteView(generic.BulkDeleteView):
    queryset = NameServer.objects.all()
    table = NameServerTable


#
# Record
#


class RecordListView(generic.ObjectListView):
    queryset = Record.objects.all()
    filterset = RecordFilter
    filterset_form = RecordFilterForm
    table = RecordTable
    template_name = "netbox_dns/object_list.html"
    action_buttons = ("add", "import")


class RecordView(generic.ObjectView):
    """Display Zone details"""

    queryset = Record.objects.all()


class RecordEditView(generic.ObjectEditView):
    """View for editing a Record instance."""

    queryset = Record.objects.all()
    model_form = RecordForm


class RecordDeleteView(generic.ObjectDeleteView):
    queryset = Record.objects.all()


class RecordBulkImportView(generic.BulkImportView):
    queryset = Record.objects.all()
    model_form = RecordCSVForm
    table = RecordTable


class RecordBulkEditView(generic.BulkEditView):
    queryset = Record.objects.all()
    filterset = RecordFilter
    table = RecordTable
    form = RecordBulkEditForm


class RecordBulkDeleteView(generic.BulkDeleteView):
    queryset = Record.objects.all()
    table = RecordTable
