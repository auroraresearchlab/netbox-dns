import django_tables2 as tables
from utilities.tables import BaseTable
from .models import NameServer, Zone


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
