import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ChoiceFieldColumn,
    ToggleColumn,
    TagColumn,
    ActionsColumn,
)

from netbox_dns.models import Record


class RecordBaseTable(NetBoxTable):
    """Base class for tables displaying Records"""

    zone = tables.Column(
        linkify=True,
    )
    type = tables.Column()
    name = tables.Column(
        linkify=True,
    )
    value = tables.TemplateColumn(
        template_code="{{ value|truncatechars:64 }}",
    )
    ttl = tables.Column(
        verbose_name="TTL",
    )
    active = tables.BooleanColumn(
        verbose_name="Active",
    )


class RecordTable(RecordBaseTable):
    """Table for displaying Record objects."""

    pk = ToggleColumn()
    status = ChoiceFieldColumn()
    disable_ptr = tables.BooleanColumn(
        verbose_name="Disable PTR",
    )
    tags = TagColumn(
        url_name="plugins:netbox_dns:record_list",
    )
    ptr_record = tables.Column(
        verbose_name="PTR Record",
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = Record
        fields = (
            "pk",
            "zone",
            "name",
            "ttl",
            "type",
            "value",
            "status",
            "disable_ptr",
            "ptr_record",
            "tags",
            "active",
            "description",
        )
        default_columns = (
            "zone",
            "name",
            "ttl",
            "type",
            "value",
            "tags",
            "active",
        )


class ManagedRecordTable(RecordBaseTable):
    """Table for displaying managed Record objects."""

    address_record = tables.Column(
        verbose_name="Address Record",
        linkify=True,
    )
    actions = ActionsColumn(actions=("changelog",))

    class Meta(NetBoxTable.Meta):
        model = Record
        fields = (
            "zone",
            "name",
            "ttl",
            "type",
            "value",
            "address_record",
            "active",
        )
        default_columns = (
            "zone",
            "name",
            "ttl",
            "type",
            "value",
            "active",
        )


class ZoneRecordTable(RecordBaseTable):
    """Table for displaying Record objects for a given zone."""

    pk = ToggleColumn()
    tags = TagColumn(
        url_name="plugins:netbox_dns:record_list",
    )
    ptr_record = tables.Column(
        verbose_name="PTR Record",
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = Record
        fields = (
            "pk",
            "name",
            "ttl",
            "type",
            "value",
            "status",
            "disable_ptr",
            "ptr_record",
            "tags",
            "active",
            "description",
        )
        default_columns = (
            "name",
            "ttl",
            "type",
            "value",
            "active",
        )


class ZoneManagedRecordTable(RecordBaseTable):
    """Table for displaying managed Record objects for a given zone."""

    address_record = tables.Column(
        verbose_name="Address Record",
        linkify=True,
    )
    actions = ActionsColumn(actions=("changelog",))

    class Meta(NetBoxTable.Meta):
        model = Record
        fields = (
            "name",
            "ttl",
            "type",
            "value",
            "address_record",
            "active",
        )
