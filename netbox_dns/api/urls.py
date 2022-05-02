from netbox.api.routers import NetBoxRouter

from netbox_dns.api.views import (
    NetboxDNSRootView,
    ViewViewSet,
    ZoneViewSet,
    NameServerViewSet,
    RecordViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxDNSRootView

router.register("views", ViewViewSet)
router.register("zones", ZoneViewSet)
router.register("nameservers", NameServerViewSet)
router.register("records", RecordViewSet)

urlpatterns = router.urls
