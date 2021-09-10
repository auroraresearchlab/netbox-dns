from django import forms

from extras.forms import CustomFieldModelForm, CustomFieldModelCSVForm
from extras.models.tags import Tag
from utilities.forms import (
    BootstrapMixin,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    StaticSelect,
    CSVChoiceField,
    CSVModelChoiceField,
)

from .models import NameServer, Record, Zone
from .fields import CustomDynamicModelMultipleChoiceField


class ZoneForm(BootstrapMixin, CustomFieldModelForm):
    """Form for creating a new Zone object."""

    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(),
        required=False,
    )

    class Meta:
        model = Zone
        fields = [
            "name",
            "status",
            "tags",
            "nameservers",
        ]


class ZoneFilterForm(BootstrapMixin, forms.ModelForm):
    """Form for filtering Zone instances."""

    q = forms.CharField(required=False, label="Search")

    status = forms.ChoiceField(choices=Zone.CHOICES)

    name = forms.CharField(
        required=False,
        label="Name",
    )

    tag = TagFilterField(Zone)

    class Meta:
        model = Zone
        fields = []


class ZoneCSVForm(CustomFieldModelCSVForm):
    status = CSVChoiceField(
        choices=Zone.CHOICES, required=True, help_text="Zone status"
    )

    class Meta:
        model = Zone
        fields = ("name", "status")


class NameServerForm(BootstrapMixin, forms.ModelForm):
    """Form for creating a new NameServer object."""

    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = NameServer
        fields = [
            "name",
            "tags",
        ]

    def clean(self):
        cleaned_data = super().clean()


class NameServerFilterForm(BootstrapMixin, forms.ModelForm):
    """Form for filtering NameServer instances."""

    q = forms.CharField(required=False, label="Search")

    name = forms.CharField(
        required=False,
        label="Name",
    )

    tag = TagFilterField(NameServer)

    class Meta:
        model = NameServer
        fields = []


class NameServerCSVForm(CustomFieldModelCSVForm):
    class Meta:
        model = NameServer
        fields = ("name",)


class RecordForm(BootstrapMixin, forms.ModelForm):
    """Form for creating a new Record object."""

    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Record
        fields = [
            "zone",
            "type",
            "name",
            "value",
            "ttl",
            "tags",
        ]

        widgets = {"zone": StaticSelect()}


class RecordFilterForm(BootstrapMixin, forms.ModelForm):
    """Form for filtering Record instances."""

    q = forms.CharField(required=False, label="Search")

    name = forms.CharField(
        required=False,
        label="Name",
    )

    tag = TagFilterField(Record)

    class Meta:
        model = Record
        fields = []


class RecordCSVForm(CustomFieldModelCSVForm):
    zone = CSVModelChoiceField(
        queryset=Zone.objects.all(),
        to_field_name="name",
        required=True,
        help_text="Assigned zone",
    )

    type = CSVChoiceField(
        choices=Record.CHOICES, required=True, help_text="Record Type"
    )

    class Meta:
        model = Record
        fields = ("zone", "type", "name", "value", "ttl")
