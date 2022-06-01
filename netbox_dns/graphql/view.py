from graphene import ObjectType

from netbox.graphql.fields import ObjectField, ObjectListField
from netbox.graphql.types import NetBoxObjectType

from netbox_dns.models import View
from netbox_dns.filters import ViewFilter


class ViewType(NetBoxObjectType):
    class Meta:
        model = View
        fields = "__all__"
        filterset_class = ViewFilter


class ViewQuery(ObjectType):
    view = ObjectField(ViewType)
    view_list = ObjectListField(ViewType)
