from netbox.views import generic

from netbox_dns.filters import RecordFilter
from netbox_dns.forms import (
    RecordCSVForm,
    RecordFilterForm,
    RecordForm,
    RecordBulkEditForm,
)
from netbox_dns.models import Record
from netbox_dns.tables import RecordTable, ManagedRecordTable


class RecordListView(generic.ObjectListView):
    queryset = Record.objects.filter(managed=False)
    filterset = RecordFilter
    filterset_form = RecordFilterForm
    table = RecordTable


class ManagedRecordListView(generic.ObjectListView):
    queryset = Record.objects.filter(managed=True)
    filterset = RecordFilter
    filterset_form = RecordFilterForm
    table = ManagedRecordTable
    actions = ("export",)
    template_name = "netbox_dns/managed_record_list.html"


class RecordView(generic.ObjectView):
    """Display Record details"""

    queryset = Record.objects.all()


class RecordEditView(generic.ObjectEditView):
    """View for editing a Record instance."""

    queryset = Record.objects.filter(managed=False)
    form = RecordForm


class RecordDeleteView(generic.ObjectDeleteView):
    queryset = Record.objects.filter(managed=False)


class RecordBulkImportView(generic.BulkImportView):
    queryset = Record.objects.filter(managed=False)
    model_form = RecordCSVForm
    table = RecordTable


class RecordBulkEditView(generic.BulkEditView):
    queryset = Record.objects.filter(managed=False)
    filterset = RecordFilter
    table = RecordTable
    form = RecordBulkEditForm


class RecordBulkDeleteView(generic.BulkDeleteView):
    queryset = Record.objects.filter(managed=False)
    table = RecordTable
