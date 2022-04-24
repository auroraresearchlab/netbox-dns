from django.forms import CharField, NullBooleanField

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelCSVForm,
    NetBoxModelForm,
)
from netbox_dns.models import View

from utilities.forms import TagFilterField, BulkEditNullBooleanSelect


class ViewForm(NetBoxModelForm):
    """Form for creating a new View object."""

    class Meta:
        model = View
        fields = ("name", "default", "tags")


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
        fields = ("name", "default")


class ViewBulkEditForm(NetBoxModelBulkEditForm):
    model = View

    default = NullBooleanField(
        required=False, widget=BulkEditNullBooleanSelect(), label="Default View"
    )
