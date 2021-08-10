from django.urls import path

from .views import (
    # zone
    ZoneListView,
    ZoneView,
    ZoneDeleteView,
    ZoneEditView,
    # nameserver
    NameServerListView,
    NameServerView,
    NameServerEditView,
    NameServerDeleteView,
)

app_name = "netbox_dns"

urlpatterns = [
    # Zone urls
    path("zones/", ZoneListView.as_view(), name="zone_list"),
    path("zones/add/", ZoneEditView.as_view(), name="zone_add"),
    path("zones/<int:pk>/", ZoneView.as_view(), name="zone"),
    path("zones/<int:pk>/delete/", ZoneDeleteView.as_view(), name="zone_delete"),
    path("zones/<int:pk>/edit/", ZoneEditView.as_view(), name="zone_edit"),
    # NameServer urls
    path("nameservers/", NameServerListView.as_view(), name="nameserver_list"),
    path("nameservers/add/", NameServerEditView.as_view(), name="nameserver_add"),
    path("nameservers/<int:pk>/", NameServerView.as_view(), name="nameserver"),
    path(
        "nameservers/<int:pk>/edit",
        NameServerEditView.as_view(),
        name="nameserver_edit",
    ),
    path(
        "nameservers/<int:pk>/delete",
        NameServerDeleteView.as_view(),
        name="nameserver_delete",
    ),
]
