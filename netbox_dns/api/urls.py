from netbox.api.routers import NetBoxRouter
from netbox_dns.api.views import (
    NetboxDNSRootView,
    ZoneViewSet,
    NameServerViewSet,
    RecordViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxDNSRootView

router.register("zones", ZoneViewSet)
router.register("nameservers", NameServerViewSet)
router.register("records", RecordViewSet)
urlpatterns = router.urls
