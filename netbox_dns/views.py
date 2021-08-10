from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, CreateView, DeleteView, UpdateView
from django_tables2 import RequestConfig
from django.contrib.auth.mixins import PermissionRequiredMixin

from netbox.views import generic

from .models import Zone, NameServer
from .tables import NameServerTable, ZoneTable
from .forms import NameServerFilterForm, NameServerForm, ZoneForm, ZoneFilterForm
from .filters import NameServerFilter, ZoneFilter


#
# Zone
#


class ZoneListView(generic.ObjectListView):
    """View for listing all existing Zones."""

    permission_required = "netbox_dns.view_zone"

    queryset = Zone.objects.all()
    filterset = ZoneFilter
    filterset_form = ZoneFilterForm
    table = ZoneTable
    template_name = "netbox_dns/object_list.html"
    action_buttons = ("add",)


class ZoneView(generic.ObjectView):
    """Display Zone details"""

    permission_required = "netbox_dns.view_zone"

    queryset = Zone.objects.all()

    def get(self, request, pk):
        """Get request."""
        zone = get_object_or_404(self.queryset, pk=pk)

        return render(
            request,
            "netbox_dns/zone.html",
            {
                "zone": zone,
            },
        )


class ZoneEditView(generic.ObjectEditView):
    """View for editing and creating a Zone instance."""

    permission_required = "netbox_dns.change_zone"
    queryset = Zone.objects.all()
    model_form = ZoneForm


class ZoneDeleteView(generic.ObjectDeleteView):
    """View for deleting a Zone instance"""

    queryset = Zone.objects.all()


#
# NameServer
#


class NameServerListView(generic.ObjectListView):
    queryset = NameServer.objects.all()
    filterset = NameServerFilter
    filterset_form = NameServerFilterForm
    table = NameServerTable
    template_name = "netbox_dns/object_list.html"

    action_buttons = ("add",)


class NameServerView(generic.ObjectView):
    """Display NameServer details"""

    permission_required = "netbox_dns.view_nameserver"

    queryset = NameServer.objects.all()

    def get(self, request, pk):
        """Get request."""
        nameserver = get_object_or_404(self.queryset, pk=pk)

        return render(
            request,
            "netbox_dns/nameserver.html",
            {
                "nameserver": nameserver,
            },
        )


class NameServerEditView(generic.ObjectEditView):
    """View for editing a Name Server instance."""

    permission_required = "netbox_dns.change_nameserver"
    queryset = NameServer.objects.all()
    model_form = NameServerForm


class NameServerDeleteView(generic.ObjectDeleteView):
    queryset = NameServer.objects.all()
