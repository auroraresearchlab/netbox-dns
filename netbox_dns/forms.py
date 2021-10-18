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
from tenancy.forms import TenancyFilterForm, TenancyForm
from utilities.forms import (
    BootstrapMixin,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    StaticSelect,
    CSVChoiceField,
    CSVModelChoiceField,
    DatePicker,
    DynamicModelChoiceField,
    APISelect,
    StaticSelectMultiple,
    CommentField,
    add_blank_choice,
    BOOLEAN_WITH_BLANK_CHOICES,
)

from .models import NameServer, Record, Zone
from .fields import CustomDynamicModelMultipleChoiceField


class ZoneForm(BootstrapMixin, TenancyForm, CustomFieldModelForm):
    """Form for creating a new Zone object."""

    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )
    nameservers = CustomDynamicModelMultipleChoiceField(
        queryset=NameServer.objects.all(),
        required=False,
    )
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Zone
        fields = [
            "name",
            "status",
            "auto_renew",
            "expire_date",
            "ssl_expire_date",
            "nameservers",
            "tenant_group",
            "tenant",
            "comments",
            "tags",
        ]
        fieldsets = (
            ("Zone", ("name", "status", "nameservers", "tags")),
            ("Date", ("auto_renew", "expire_date")),
            ("SSL", ("ssl_expire_date",)),
            ("Tenancy", ("tenant_group", "tenant")),
        )
        widgets = {
            "status": StaticSelect(),
            "expire_date": DatePicker(),
            "ssl_expire_date": DatePicker(),
        }


class ZoneFilterForm(BootstrapMixin, TenancyFilterForm, CustomFieldModelFilterForm):
    """Form for filtering Zone instances."""

    model = Zone
    field_groups = [
        ["q", "tag"],
        ["name", "status", "auto_renew", "expire_date", "ssl_expire_date"],
        ["tenant_group_id", "tenant_id"],
    ]

    q = forms.CharField(
        required=False,
        label="Search",
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(Zone.CHOICES),
        required=False,
        widget=StaticSelect(),
    )
    name = forms.CharField(
        required=False,
        label="Name",
    )
    auto_renew = forms.NullBooleanField(
        required=False,
        widget=StaticSelect(
            choices=BOOLEAN_WITH_BLANK_CHOICES,
        ),
    )
    expire_date = forms.DateTimeField(
        required=False,
        widget=DatePicker(),
    )
    ssl_expire_date = forms.DateTimeField(
        required=False,
        widget=DatePicker(),
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
