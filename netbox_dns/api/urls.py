from rest_framework import routers
from netbox_dns.api.views import ZoneViewSet, NameServerViewSet, RecordViewSet

router = routers.DefaultRouter()
router.register("zones", ZoneViewSet)
router.register("nameservers", NameServerViewSet)
router.register("records", RecordViewSet)
urlpatterns = router.urls
