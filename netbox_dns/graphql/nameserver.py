from graphene import ObjectType

from netbox.graphql.fields import ObjectField, ObjectListField
from netbox.graphql.types import NetBoxObjectType

from netbox_dns.models import NameServer
from netbox_dns.filters import NameServerFilter


class NameServerType(NetBoxObjectType):
    class Meta:
        model = NameServer
        fields = "__all__"
        filterset_class = NameServerFilter


class NameServerQuery(ObjectType):
    nameserver = ObjectField(NameServerType)
    nameserver_list = ObjectListField(NameServerType)
