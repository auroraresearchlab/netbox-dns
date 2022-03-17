from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import CharField

from extras.models.tags import Tag
from netbox.forms import NetBoxModelBulkEditForm
from utilities.forms import (
    CSVModelForm,
    BootstrapMixin,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)

from netbox_dns.models import NameServer


class NameServerForm(BootstrapMixin, forms.ModelForm):
    """Form for creating a new NameServer object."""

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = NameServer
        fields = ("name", "tags")


class NameServerFilterForm(BootstrapMixin, forms.Form):
    """Form for filtering NameServer instances."""

    model = NameServer

    name = CharField(
        required=False,
        label="Name",
    )
    tag = TagFilterField(NameServer)


class NameServerCSVForm(CSVModelForm, BootstrapMixin, forms.ModelForm):
    class Meta:
        model = NameServer
        fields = ("name",)


class NameServerBulkEditForm(NetBoxModelBulkEditForm):
    model = NameServer
