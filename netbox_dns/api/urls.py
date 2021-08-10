from rest_framework import routers
from netbox_dns.api.views import NameServerViewSet, ZoneViewSet

router = routers.DefaultRouter()
router.register("zones", ZoneViewSet)
router.register("nameservers", NameServerViewSet)
urlpatterns = router.urls
