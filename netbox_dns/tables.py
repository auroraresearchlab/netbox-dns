import django_tables2 as tables
from utilities.tables import BaseTable, ChoiceFieldColumn, ToggleColumn, TagColumn
from .models import NameServer, Record, Zone


class ZoneTable(BaseTable):
    """Table for displaying Zone objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    status = ChoiceFieldColumn()
    tenant = tables.Column(
        linkify=True,
    )
    auto_renew = tables.BooleanColumn()
    expire_date = tables.DateColumn(
        short=False,
    )
    ssl_expire_date = tables.DateColumn(
        short=False,
    )
    tags = TagColumn(
        url_name="plugins:netbox_dns:zone_list",
    )

    class Meta(BaseTable.Meta):
        model = Zone
        fields = (
            "pk",
            "name",
            "status",
            "tenant",
            "auto_renew",
            "expire_date",
            "ssl_expire_date",
            "tags",
        )
        default_columns = (
            "pk",
            "name",
            "status",
            "auto_renew",
            "expire_date",
            "tags",
        )


class NameServerTable(BaseTable):
    """Table for displaying NameServer objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    tags = TagColumn(
        url_name="plugins:netbox_dns:nameserver_list",
    )

    class Meta(BaseTable.Meta):
        model = NameServer
        fields = (
            "pk",
            "name",
            "tags",
        )


class RecordTable(BaseTable):
    """Table for displaying Record objects."""

    pk = ToggleColumn()
    zone = tables.LinkColumn()
    type = tables.LinkColumn()
    name = tables.LinkColumn()
    tags = TagColumn(
        url_name="plugins:netbox_dns:record_list",
    )

    class Meta(BaseTable.Meta):
        model = Record
        fields = (
            "pk",
            "zone",
            "type",
            "name",
            "value",
            "tags",
        )
