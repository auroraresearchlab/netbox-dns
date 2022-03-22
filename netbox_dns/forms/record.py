from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import (
    validate_ipv6_address,
    validate_ipv4_address,
)
from django.forms import (
    CharField,
    IntegerField,
    BooleanField,
    NullBooleanField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelCSVForm,
    NetBoxModelForm,
)
from utilities.forms import (
    BulkEditNullBooleanSelect,
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

from netbox_dns.models import Record, RecordTypeChoices, Zone


class RecordForm(NetBoxModelForm):
    """Form for creating a new Record object."""

    disable_ptr = BooleanField(
        label="Disable PTR",
        required=False,
    )
    ttl = IntegerField(
        required=False,
        label="TTL",
    )

    def clean(self):
        """
        For A and AAA records, verify that a valid IPv4 or IPv6 was passed as
        value and raise a ValidationError exception otherwise.
        """
        cleaned_data = super().clean()

        type = cleaned_data.get("type")
        if type not in (RecordTypeChoices.A, RecordTypeChoices.AAAA):
            return

        value = cleaned_data.get("value")
        try:
            ip_version = "4" if type == RecordTypeChoices.A else "6"
            if type == RecordTypeChoices.A:
                validate_ipv4_address(value)
            else:
                validate_ipv6_address(value)

        except ValidationError:
            raise forms.ValidationError(
                {
                    "value": f"A valid IPv{ip_version} address is required for record type {type}."
                }
            )

        if cleaned_data.get("disable_ptr"):
            return

        conflicts = Record.objects.filter(value=value, type=type, disable_ptr=False)
        if self.instance.pk:
            conflicts = conflicts.exclude(pk=self.instance.pk)
        if len(conflicts):
            raise forms.ValidationError(
                {
                    "value": f"There is already an {type} record with value {value} and PTR enabled."
                }
            )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")

            return ttl

        return self.cleaned_data["zone"].default_ttl

    class Meta:
        model = Record
        fields = ("zone", "type", "disable_ptr", "name", "value", "ttl", "tags")

        widgets = {
            "zone": StaticSelect(),
            "type": StaticSelect(),
        }


class RecordFilterForm(NetBoxModelFilterSetForm):
    """Form for filtering Record instances."""

    type = forms.MultipleChoiceField(
        choices=add_blank_choice(RecordTypeChoices),
        required=False,
        widget=StaticSelectMultiple(),
    )
    name = CharField(
        required=False,
        label="Name",
    )
    value = CharField(
        required=False,
        label="Value",
    )
    zone_id = DynamicModelMultipleChoiceField(
        queryset=Zone.objects.all(),
        required=False,
        label="Zone",
    )
    tag = TagFilterField(Record)

    model = Record


class RecordCSVForm(NetBoxModelCSVForm):
    zone = CSVModelChoiceField(
        queryset=Zone.objects.all(),
        to_field_name="name",
        required=True,
        help_text="Assigned zone",
    )
    type = CSVChoiceField(
        choices=RecordTypeChoices,
        required=True,
        help_text="Record Type",
    )
    ttl = IntegerField(
        required=False,
        help_text="TTL",
    )
    disable_ptr = forms.BooleanField(
        required=False,
        label="Disable PTR",
        help_text="Disable generation of a PTR record",
    )

    def clean(self):
        """
        For A and AAA records, verify that a valid IPv4 or IPv6 was passed as
        value and raise a ValidationError exception otherwise.
        """
        cleaned_data = super().clean()

        type = cleaned_data.get("type")
        if type not in (RecordTypeChoices.A, RecordTypeChoices.AAAA):
            return

        value = cleaned_data.get("value")
        try:
            ip_version = "4" if type == RecordTypeChoices.A else "6"
            if type == RecordTypeChoices.A:
                validate_ipv4_address(value)
            else:
                validate_ipv6_address(value)

        except ValidationError:
            raise forms.ValidationError(
                {
                    "value": f"A valid IPv{ip_version} address is required for record type {type}."
                }
            )

        if cleaned_data.get("disable_ptr"):
            return

        conflicts = Record.objects.filter(value=value, type=type, disable_ptr=False)
        if len(conflicts):
            raise forms.ValidationError(
                {
                    "value": f"There is already an {type} record with value {value} and PTR enabled."
                }
            )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")

            return ttl

        if "zone" in self.cleaned_data:
            return self.cleaned_data["zone"].default_ttl

        return None

    class Meta:
        model = Record
        fields = ("zone", "type", "name", "value", "ttl", "disable_ptr")


class RecordBulkEditForm(NetBoxModelBulkEditForm):
    zone = DynamicModelChoiceField(
        queryset=Zone.objects.all(),
        required=False,
        widget=APISelect(
            attrs={"data-url": reverse_lazy("plugins-api:netbox_dns-api:zone-list")}
        ),
    )
    disable_ptr = NullBooleanField(
        required=False, widget=BulkEditNullBooleanSelect(), label="Disable PTR"
    )
    ttl = IntegerField(
        required=False,
        label="TTL",
    )

    model = Record
    fieldsets = ((None, ("zone", "disable_ptr", "ttl")),)

    def clean(self):
        """
        For A and AAA records, verify that a valid IPv4 or IPv6 was passed as
        value and raise a ValidationError exception otherwise.

        Check for internal clashes between A/AAAA records with the same value
        and for conflicts with existing A/AAAA records in the database as well.
        """
        cleaned_data = super().clean()

        disable_ptr = cleaned_data.get("disable_ptr")
        if disable_ptr is None or disable_ptr:
            return

        address_values = [
            record.value
            for record in cleaned_data.get("pk")
            if record.type in (RecordTypeChoices.A, RecordTypeChoices.AAAA)
        ]

        conflicts = [
            f"Multiple records with value {value} and PTR enabled."
            for value in set(address_values)
            if address_values.count(value) > 1
        ]
        if conflicts:
            raise forms.ValidationError({"disable_ptr": conflicts})

        for record in cleaned_data.get("pk"):
            conflicts = (
                Record.objects.filter(Record.unique_ptr_qs)
                .filter(value=record.value)
                .exclude(pk=record.pk)
            )
            if len(conflicts):
                raise forms.ValidationError(
                    {
                        "disable_ptr": f"Multiple {record.type} records with value {record.value} and PTR enabled."
                    }
                )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")

            return ttl

        return None
