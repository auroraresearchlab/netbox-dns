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
    queryset = Record.objects.filter(managed=False).prefetch_related(
        "zone", "ptr_record"
    )
    filterset = RecordFilter
    filterset_form = RecordFilterForm
    table = RecordTable


class ManagedRecordListView(generic.ObjectListView):
    queryset = Record.objects.filter(managed=True).prefetch_related(
        "zone", "address_record"
    )
    filterset = RecordFilter
    filterset_form = RecordFilterForm
    table = ManagedRecordTable
    actions = ("export",)
    template_name = "netbox_dns/managed_record_list.html"


class RecordView(generic.ObjectView):
    """Display Record details"""

    queryset = Record.objects.all().prefetch_related("zone", "ptr_record")


class RecordEditView(generic.ObjectEditView):
    """View for editing a Record instance."""

    queryset = Record.objects.filter(managed=False).prefetch_related(
        "zone", "ptr_record"
    )
    form = RecordForm


class RecordDeleteView(generic.ObjectDeleteView):
    queryset = Record.objects.filter(managed=False)
    default_return_url = "plugins:netbox_dns:record_list"


class RecordBulkImportView(generic.BulkImportView):
    queryset = Record.objects.filter(managed=False).prefetch_related(
        "zone", "ptr_record"
    )
    model_form = RecordCSVForm
    table = RecordTable


class RecordBulkEditView(generic.BulkEditView):
    queryset = Record.objects.filter(managed=False).prefetch_related("zone")
    filterset = RecordFilter
    table = RecordTable
    form = RecordBulkEditForm


class RecordBulkDeleteView(generic.BulkDeleteView):
    queryset = Record.objects.filter(managed=False)
    table = RecordTable
