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
        fields = ("name", "description", "tags")


class NameServerFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering NameServer instances."""

    model = NameServer

    name = CharField(
        required=False,
        label="Name",
    )
    tag = TagFilterField(NameServer)


class NameServerCSVForm(NetBoxModelCSVForm):
    class Meta:
        model = NameServer

        fields = ("name", "description")


class NameServerBulkEditForm(NetBoxModelBulkEditForm):
    model = NameServer

    description = CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = ("description",)
