from netbox.views import generic

from netbox_dns.models import View
from netbox_dns.filters import ViewFilter
from netbox_dns.forms import ViewForm, ViewFilterForm, ViewCSVForm, ViewBulkEditForm
from netbox_dns.tables import ViewTable


class ViewView(generic.ObjectView):
    queryset = View.objects.all()


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
