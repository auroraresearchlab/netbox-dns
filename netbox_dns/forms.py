from django import forms

from extras.forms import CustomFieldModelForm
from extras.models.tags import Tag
from utilities.forms import (
    BootstrapMixin,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)

from .models import NameServer, Zone
from .fields import CustomDynamicModelMultipleChoiceField


class ZoneForm(BootstrapMixin, CustomFieldModelForm):
    """Form for creating a new Zone object."""

    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(), required=False
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
