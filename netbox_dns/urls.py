from django.urls import path

from extras.views import ObjectChangeLogView
from netbox_dns.models import Zone, Record, NameServer
from .views import (
    # zone
    ZoneListView,
    ZoneView,
    ZoneDeleteView,
    ZoneEditView,
    ZoneBulkImportView,
    ZoneBulkEditView,
    ZoneBulkDeleteView,
    ZoneRecordListView,
    ZoneManagedRecordListView,
    # nameserver
    NameServerListView,
    NameServerView,
    NameServerEditView,
    NameServerDeleteView,
    NameServerBulkImportView,
    NameServerBulkDeleteView,
    # record
    RecordListView,
    RecordView,
    RecordEditView,
    RecordDeleteView,
    RecordBulkImportView,
    RecordBulkEditView,
    RecordBulkDeleteView,
    # managed record
    ManagedRecordListView,
)

app_name = "netbox_dns"

urlpatterns = [
    #
    # Zone urls
    #
    path("zones/", ZoneListView.as_view(), name="zone_list"),
    path("zones/add/", ZoneEditView.as_view(), name="zone_add"),
    path("zones/import/", ZoneBulkImportView.as_view(), name="zone_import"),
    path("zones/edit/", ZoneBulkEditView.as_view(), name="zone_bulk_edit"),
    path("zones/delete/", ZoneBulkDeleteView.as_view(), name="zone_bulk_delete"),
    path("zones/<int:pk>/", ZoneView.as_view(), name="zone"),
    path("zones/<int:pk>/delete/", ZoneDeleteView.as_view(), name="zone_delete"),
    path("zones/<int:pk>/edit/", ZoneEditView.as_view(), name="zone_edit"),
    path(
        "zones/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="zone_changelog",
        kwargs={"model": Zone},
    ),
    path(
        "zones/<int:pk>/records/", ZoneRecordListView.as_view(), name="zone_record_list"
    ),
    path(
        "zones/<int:pk>/managedrecords/",
        ZoneManagedRecordListView.as_view(),
        name="zone_managed_record_list",
    ),
    #
    # NameServer urls
    #
    path("nameservers/", NameServerListView.as_view(), name="nameserver_list"),
    path("nameservers/add/", NameServerEditView.as_view(), name="nameserver_add"),
    path(
        "nameservers/import/",
        NameServerBulkImportView.as_view(),
        name="nameserver_import",
    ),
    path(
        "nameservers/delete/",
        NameServerBulkDeleteView.as_view(),
        name="nameserver_bulk_delete",
    ),
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
    path(
        "nameservers/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="nameserver_changelog",
        kwargs={"model": NameServer},
    ),
    #
    # Record urls
    #
    path("records/", RecordListView.as_view(), name="record_list"),
    path("records/add/", RecordEditView.as_view(), name="record_add"),
    path("records/import/", RecordBulkImportView.as_view(), name="record_import"),
    path("records/edit/", RecordBulkEditView.as_view(), name="record_bulk_edit"),
    path("records/delete/", RecordBulkDeleteView.as_view(), name="record_bulk_delete"),
    path("records/<int:pk>/", RecordView.as_view(), name="record"),
    path("records/<int:pk>/edit/", RecordEditView.as_view(), name="record_edit"),
    path("records/<int:pk>/delete/", RecordDeleteView.as_view(), name="record_delete"),
    path(
        "records/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="record_changelog",
        kwargs={"model": Record},
    ),
    path(
        "managedrecords/", ManagedRecordListView.as_view(), name="managed_record_list"
    ),
]
