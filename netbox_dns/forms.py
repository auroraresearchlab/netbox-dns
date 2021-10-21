from django import forms
from django.forms import IntegerField, ValidationError, widgets
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv6_address, validate_ipv4_address

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

    def __init__(self, *args, **kwargs):
        """Override the __init__ method in order to provide the initial value for the default_ttl field"""
        super().__init__(*args, **kwargs)
        self.initial["default_ttl"] = (
            settings.PLUGINS_CONFIG.get("netbox_dns").get("zone").get("default_ttl")
        )

    def clean_default_ttl(self):
        if self.cleaned_data["default_ttl"]:
            return self.cleaned_data["default_ttl"]
        else:
            return self.initial["default_ttl"]

    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(),
        required=False,
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )
    default_ttl = forms.IntegerField(
        required=False,
        label="Default TTL",
        help_text="Default TTL for new records in this zone",
    )

    class Meta:
        model = Zone
        fields = ("name", "status", "nameservers", "default_ttl", "tags")

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
    default_ttl = IntegerField(
        help_text="Default TTL",
        required=False,
    )

    def clean_default_ttl(self):
        default_ttl = self.cleaned_data.get("default_ttl", 0)
        if default_ttl is not None:
            if default_ttl <= 0:
                raise ValidationError("Default TTL must be greater than zero")
        else:
            default_ttl = (
                settings.PLUGINS_CONFIG.get("netbox_dns").get("zone").get("default_ttl")
            )

        return default_ttl

    class Meta:
        model = Zone
        fields = ("name", "status", "default_ttl")


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
    default_ttl = forms.IntegerField(
        required=False,
        label="Default TTL",
    )

    def clean_default_ttl(self):
        default_ttl = self.cleaned_data.get("default_ttl")
        if default_ttl is not None and default_ttl <= 0:
            raise ValidationError("Default TTL must be greater than zero")

        return default_ttl

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

    def clean(self):
        """
        For A and AAA records, verify that a valid IPv4 or IPv6 was passed as
        value and raise a ValidationError exception otherwise.
        """
        cleaned_data = super().clean()

        type = cleaned_data.get("type")
        if type not in (Record.A, Record.AAAA):
            return

        value = cleaned_data.get("value")
        try:
            ip_version = "4" if type == Record.A else "6"
            if type == Record.A:
                validate_ipv4_address(value)
            else:
                validate_ipv6_address(value)

        except ValidationError:
            raise ValidationError(
                f"A valid IPv{ip_version} address is required for record type {type}."
            )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")
            return ttl
        else:
            return self.cleaned_data["zone"].default_ttl

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )
    ttl = forms.IntegerField(
        required=False,
        label="TTL",
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
    ttl = IntegerField(
        required=False,
        help_text="TTL",
    )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")
            return ttl
        elif "zone" in self.cleaned_data:
            return self.cleaned_data["zone"].default_ttl

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
    ttl = IntegerField(
        required=False,
        help_text="TTL",
    )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")
            return ttl
        else:
            return self.cleaned_data["zone"].default_ttl

    class Meta:
        nullable_fields = []
