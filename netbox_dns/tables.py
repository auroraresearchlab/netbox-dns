import django_tables2 as tables
from utilities.tables import BaseTable, ChoiceFieldColumn, ToggleColumn
from .models import NameServer, Record, Zone


class ZoneTable(BaseTable):
    """Table for displaying Zone objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    status = ChoiceFieldColumn()
    tenant = tables.Column(linkify=True)
    expire_date = tables.DateColumn(short=False)

    class Meta(BaseTable.Meta):
        model = Zone
        fields = (
            "pk",
            "name",
            "status",
            "tenant",
            "expire_date",
        )


class NameServerTable(BaseTable):
    """Table for displaying NameServer objects."""

    pk = ToggleColumn()
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = NameServer
        fields = (
            "pk",
            "name",
        )


class RecordTable(BaseTable):
    """Table for displaying Record objects."""

    pk = ToggleColumn()
    zone = tables.LinkColumn()
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Record
        fields = (
            "pk",
            "zone",
            "name",
            "value",
        )
