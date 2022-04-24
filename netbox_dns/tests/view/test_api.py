from utilities.testing import APIViewTestCases

from netbox_dns.tests.custom import APITestCase
from netbox_dns.models import View


class ViewTest(
    APITestCase,
    APIViewTestCases.GetObjectViewTestCase,
    APIViewTestCases.ListObjectsViewTestCase,
    APIViewTestCases.CreateObjectViewTestCase,
    APIViewTestCases.UpdateObjectViewTestCase,
    APIViewTestCases.DeleteObjectViewTestCase,
):
    model = View
    brief_fields = ["default", "display", "id", "name", "url"]

    create_data = [
        {"name": "external"},
        {"name": "internal"},
        {"name": "diverse"},
    ]

    @classmethod
    def setUpTestData(cls):
        views = (
            View(name="test1", default=True),
            View(name="test2", default=False),
            View(name="test3", default=False),
        )
        View.objects.bulk_create(views)
