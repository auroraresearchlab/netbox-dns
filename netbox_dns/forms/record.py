from django import forms

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

    class Meta:
        model = Record
        fields = ("name", "zone", "type", "value", "ttl", "disable_ptr", "tags")

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        view = None
        if self.is_bound and "view" in self.data:
            try:
                view = self.fields["view"].to_python(self.data["view"])
            except forms.ValidationError:
                pass

        if view:
            self.fields["zone"].queryset = Zone.objects.filter(view=view)
        else:
            self.fields["zone"].queryset = Zone.objects.filter(view__isnull=True)

    zone = CSVModelChoiceField(
        queryset=Zone.objects.all(),
        to_field_name="name",
        required=True,
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

    def is_valid(self):
        try:
            is_valid = super().is_valid()
        except Record.zone.RelatedObjectDoesNotExist:
            is_valid = False

        return is_valid

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
    type = forms.ChoiceField(
        choices=RecordTypeChoices,
        required=False,
        widget=StaticSelect(),
    )
    value = CharField(
        required=False,
        label="Value",
    )
    ttl = IntegerField(
        required=False,
        label="TTL",
    )
    disable_ptr = NullBooleanField(
        required=False, widget=BulkEditNullBooleanSelect(), label="Disable PTR"
    )

    model = Record
    fieldsets = ((None, ("zone", "type", "value", "ttl", "disable_ptr")),)
