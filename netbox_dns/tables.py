import django_tables2 as tables
from utilities.tables import BaseTable, ChoiceFieldColumn, ToggleColumn
from .models import NameServer, Record, Zone


class ZoneTable(BaseTable):
    """Table for displaying Zone objects."""

    id = tables.LinkColumn()
    name = tables.LinkColumn()
    status = ChoiceFieldColumn()
    tenant = tables.Column(linkify=True)
    expire_date = tables.DateColumn(short=False)

    class Meta(BaseTable.Meta):
        model = Zone
        fields = (
            "id",
            "name",
            "status",
            "tenant",
            "expire_date",
        )


class NameServerTable(BaseTable):
    """Table for displaying NameServer objects."""

    id = tables.LinkColumn()
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = NameServer
        fields = (
            "id",
            "name",
        )


class RecordTable(BaseTable):
    """Table for displaying Record objects."""

    id = tables.LinkColumn()
    zone = tables.LinkColumn()
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Record
        fields = (
            "id",
            "zone",
            "name",
            "value",
        )
