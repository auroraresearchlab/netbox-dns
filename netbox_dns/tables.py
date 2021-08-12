import django_tables2 as tables
from utilities.tables import BaseTable
from .models import NameServer, Record, Zone


class ZoneTable(BaseTable):
    """Table for displaying Zone objects."""

    id = tables.LinkColumn()
    name = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Zone
        fields = (
            "id",
            "name",
            "status",
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
