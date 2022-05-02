from django import forms
from django.core.exceptions import ValidationError

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

from netbox_dns.models import View, Zone, Record, RecordTypeChoices


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
        cleaned_data = super().clean()

        type = cleaned_data.get("type")
        if type not in (RecordTypeChoices.A, RecordTypeChoices.AAAA):
            return

        if cleaned_data.get("disable_ptr"):
            return

        value = cleaned_data.get("value")
        zone = cleaned_data.get("zone")

        conflicts = Record.objects.filter(value=value, type=type, disable_ptr=False)
        if zone.view is None:
            conflicts = conflicts.filter(zone__view__isnull=True)
        else:
            conflicts = conflicts.filter(zone__view_id=zone.view.pk)

        if self.instance.pk:
            conflicts = conflicts.exclude(pk=self.instance.pk)
        if len(conflicts):
            raise forms.ValidationError(
                {
                    "value": f"There is already an {type} record with value {value} and PTR enabled."
                }
            ) from None

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
    view_id = DynamicModelMultipleChoiceField(
        queryset=View.objects.all(),
        required=False,
        label="View",
    )
    tag = TagFilterField(Record)

    model = Record


class RecordCSVForm(NetBoxModelCSVForm):
    zone = CharField(
        required=True,
        min_length=1,
        max_length=255,
        help_text="Zone",
    )
    view = CSVModelChoiceField(
        queryset=View.objects.all(),
        to_field_name="name",
        required=False,
        help_text="View the zone belongs to",
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
        Determine the unique zone object (if any) from the value of "zone" and
        "view".

        For A and AAA records, verify that a valid IPv4 or IPv6 was passed as
        value and raise a ValidationError exception otherwise.
        """
        cleaned_data = super().clean()

        zone_name = cleaned_data.get("zone")
        view = cleaned_data.get("view", None)

        if view is None:
            zones = Zone.objects.filter(name=zone_name, view__isnull=True)
        else:
            zones = Zone.objects.filter(name=zone_name, view=view)

        if len(zones):
            cleaned_data["zone"] = zones[0]
        else:
            cleaned_data["zone"] = None
            raise forms.ValidationError(
                {"zone": f"Zone {zone_name} not found in view {view}."}
            ) from None

        ttl = cleaned_data.get("ttl", None)
        if ttl is not None:
            if ttl <= 0:
                raise forms.ValidationError({"TTL must be greater than zero"}) from None

            cleaned_data["ttl"] = ttl
        else:
            cleaned_data["ttl"] = cleaned_data["zone"].default_ttl

        type = cleaned_data.get("type")
        if type not in (RecordTypeChoices.A, RecordTypeChoices.AAAA):
            return cleaned_data

        if cleaned_data.get("disable_ptr"):
            return cleaned_data

        value = cleaned_data.get("value")
        conflicts = Record.objects.filter(value=value, type=type, disable_ptr=False)
        if view is None:
            conflicts = conflicts.filter(zone__view__isnull=True)
        else:
            conflicts = conflicts.filter(zone__view_id=view.pk)

        if len(conflicts):
            raise forms.ValidationError(
                {
                    "value": f"There is already an {type} record with value {value} and PTR enabled."
                }
            ) from None

        return cleaned_data

    def clean_type(self):
        return self.cleaned_data["type"].upper()

    class Meta:
        model = Record
        fields = ("zone", "view", "type", "name", "value", "ttl", "disable_ptr")


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
        Check for internal clashes between A/AAAA records with the same value
        and for conflicts with existing A/AAAA records in the database as well.
        """
        cleaned_data = super().clean()

        disable_ptr = cleaned_data.get("disable_ptr")
        zone = cleaned_data.get("zone")

        if zone is None and (disable_ptr is None or disable_ptr):
            return

        address_values = [
            (record.value, record.zone.view)
            for record in cleaned_data.get("pk")
            if record.type in (RecordTypeChoices.A, RecordTypeChoices.AAAA)
        ]

        conflicts = [
            f"Multiple records with value {value[0]} and PTR enabled in view {value[1]}."
            for value in set(address_values)
            if address_values.count(value) > 1
        ]
        if conflicts:
            raise forms.ValidationError({"disable_ptr": conflicts})

        for record in cleaned_data.get("pk"):
            if record.zone.view is None:
                conflicts = (
                    Record.objects.filter(Record.unique_ptr_qs)
                    .filter(value=record.value, zone__view__isnull=True)
                    .exclude(pk=record.pk)
                )
            else:
                conflicts = (
                    Record.objects.filter(Record.unique_ptr_qs)
                    .filter(value=record.value, zone__view_id=record.zone.view.pk)
                    .exclude(pk=record.pk)
                )

            if len(conflicts):
                raise forms.ValidationError(
                    {
                        "disable_ptr": f"Multiple {record.type} records with value {record.value} and PTR enabled in view {record.zone.view}."
                    }
                )

    def clean_ttl(self):
        ttl = self.cleaned_data["ttl"]
        if ttl is not None:
            if ttl <= 0:
                raise ValidationError("TTL must be greater than zero")

            return ttl

        return None
