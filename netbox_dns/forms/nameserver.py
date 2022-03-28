from django.forms import CharField

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelCSVForm,
    NetBoxModelForm,
)

from utilities.forms import TagFilterField

from netbox_dns.models import NameServer


class NameServerForm(NetBoxModelForm):
    """Form for creating a new NameServer object."""

    class Meta:
        model = NameServer
        fields = ("name", "tags")


class NameServerFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering NameServer instances."""

    name = CharField(
        required=False,
        label="Name",
    )
    tag = TagFilterField(NameServer)

    model = NameServer


class NameServerCSVForm(NetBoxModelCSVForm):
    class Meta:
        model = NameServer
        fields = ("name",)


class NameServerBulkEditForm(NetBoxModelBulkEditForm):
    model = NameServer
