from django.forms import CharField

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelCSVForm,
    NetBoxModelForm,
)
from utilities.forms import TagFilterField

from netbox_dns.models import View


class ViewForm(NetBoxModelForm):
    """Form for creating a new View object."""

    class Meta:
        model = View
        fields = ("name", "tags")


class ViewFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering View instances."""

    name = CharField(
        required=False,
        label="Name",
    )
    tag = TagFilterField(View)

    model = View


class ViewCSVForm(NetBoxModelCSVForm):
    class Meta:
        model = View
        fields = ("name",)


class ViewBulkEditForm(NetBoxModelBulkEditForm):
    model = View
