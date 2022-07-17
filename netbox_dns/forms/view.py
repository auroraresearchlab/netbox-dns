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
        fields = ("name", "description", "tags")


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
        fields = ("name", "description")


class ViewBulkEditForm(NetBoxModelBulkEditForm):
    model = View

    description = CharField(max_length=200, required=False)

    class Meta:
        nullable_fields = ["description"]
