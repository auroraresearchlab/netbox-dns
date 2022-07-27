import django_tables2 as tables

from netbox.tables import NetBoxTable
from netbox_dns.models import View


class ViewTable(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = View
        fields = ("name", "description")
        default_columns = ("name",)
