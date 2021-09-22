from django import forms
from django.forms import widgets

from extras.forms import (
    CustomFieldModelForm,
    CustomFieldModelCSVForm,
    AddRemoveTagsForm,
    CustomFieldModelBulkEditForm,
    CustomFieldModelFilterForm,
)
from extras.models.tags import Tag
from utilities.forms import (
    BootstrapMixin,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    StaticSelect,
    CSVChoiceField,
    CSVModelChoiceField,
    DynamicModelChoiceField,
    APISelect,
    StaticSelectMultiple,
    add_blank_choice,
)

from .models import NameServer, Record, Zone
from .fields import CustomDynamicModelMultipleChoiceField


class ZoneForm(BootstrapMixin, CustomFieldModelForm):
    """Form for creating a new Zone object."""

    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(),
        required=False,
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Zone
        fields = ("name", "status", "tags", "nameservers")

        widgets = {
            "status": StaticSelect(),
        }


class ZoneFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    """Form for filtering Zone instances."""

    model = Zone

    q = forms.CharField(required=False, label="Search")
    status = forms.ChoiceField(
        choices=add_blank_choice(Zone.CHOICES),
        required=False,
        widget=StaticSelect(),
    )
    name = forms.CharField(
        required=False,
        label="Name",
    )
    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(),
        required=False,
    )
    tag = TagFilterField(Zone)


class ZoneCSVForm(CustomFieldModelCSVForm):
    status = CSVChoiceField(
        choices=Zone.CHOICES,
        help_text="Zone status",
    )

    class Meta:
        model = Zone
        fields = ("name", "status")


class ZoneBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Zone.objects.all(),
        widget=forms.MultipleHiddenInput(),
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(Zone.CHOICES),
        required=False,
        widget=StaticSelect(),
    )
    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(),
        required=False,
    )

    class Meta:
        nullable_fields = []


class NameServerForm(BootstrapMixin, forms.ModelForm):
    """Form for creating a new NameServer object."""

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = NameServer
        fields = ("name", "tags")


class NameServerFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    """Form for filtering NameServer instances."""

    model = NameServer

    q = forms.CharField(
        required=False,
        label="Search",
    )
    name = forms.CharField(
        required=False,
        label="Name",
    )
    tag = TagFilterField(NameServer)


class NameServerCSVForm(CustomFieldModelCSVForm):
    class Meta:
        model = NameServer
        fields = ("name",)


class RecordForm(BootstrapMixin, forms.ModelForm):
    """Form for creating a new Record object."""

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Record
        fields = ("zone", "type", "name", "value", "ttl", "tags")

        widgets = {
            "zone": StaticSelect(),
            "type": StaticSelect(),
        }


class RecordFilterForm(BootstrapMixin, CustomFieldModelFilterForm):
    """Form for filtering Record instances."""

    model = Record

    q = forms.CharField(
        required=False,
        label="Search",
    )
    type = forms.MultipleChoiceField(
        choices=add_blank_choice(Record.CHOICES),
        required=False,
        widget=StaticSelectMultiple(),
    )
    name = forms.CharField(
        required=False,
        label="Name",
    )
    value = forms.CharField(
        required=False,
        label="Value",
    )
    tag = TagFilterField(Record)


class RecordCSVForm(CustomFieldModelCSVForm):
    zone = CSVModelChoiceField(
        queryset=Zone.objects.all(),
        to_field_name="name",
        required=True,
        help_text="Assigned zone",
    )
    type = CSVChoiceField(
        choices=Record.CHOICES,
        required=True,
        help_text="Record Type",
    )

    class Meta:
        model = Record
        fields = ("zone", "type", "name", "value", "ttl")


class RecordBulkEditForm(
    BootstrapMixin, AddRemoveTagsForm, CustomFieldModelBulkEditForm
):
    pk = forms.ModelMultipleChoiceField(
        queryset=Record.objects.all(), widget=forms.MultipleHiddenInput()
    )
    zone = DynamicModelChoiceField(
        queryset=Zone.objects.all(),
        required=False,
        widget=APISelect(attrs={"data-url": "plugins:netbox_dns-api:zone-list"}),
    )
    ttl = forms.IntegerField(required=False)

    class Meta:
        nullable_fields = []
