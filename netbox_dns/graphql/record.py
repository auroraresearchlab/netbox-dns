from graphene import ObjectType

from netbox.graphql.fields import ObjectField, ObjectListField
from netbox.graphql.types import NetBoxObjectType

from netbox_dns.models import Record
from netbox_dns.filters import RecordFilter


class RecordType(NetBoxObjectType):
    class Meta:
        model = Record
        fields = "__all__"
        filterset_class = RecordFilter


class RecordQuery(ObjectType):
    record = ObjectField(RecordType)
    record_list = ObjectListField(RecordType)
