from utilities.testing import ViewTestCases
from utilities.testing import create_tags

from netbox_dns.tests.custom import ModelViewTestCase
from netbox_dns.models import View


class ViewTestCase(
    ModelViewTestCase,
    ViewTestCases.GetObjectViewTestCase,
    ViewTestCases.CreateObjectViewTestCase,
    ViewTestCases.EditObjectViewTestCase,
    ViewTestCases.DeleteObjectViewTestCase,
    ViewTestCases.ListObjectsViewTestCase,
    ViewTestCases.GetObjectChangelogViewTestCase,
    ViewTestCases.BulkImportObjectsViewTestCase,
    ViewTestCases.BulkDeleteObjectsViewTestCase,
):
    model = View

    @classmethod
    def setUpTestData(cls):
        cls.views = [
            View(name="external"),
            View(name="internal"),
        ]

        View.objects.bulk_create(cls.views)

        tags = create_tags("Alpha", "Bravo", "Charlie")

        cls.form_data = {
            "name": "test1",
            "tags": [t.pk for t in tags],
        }

        cls.csv_data = (
            "name",
            "test2",
            "test3",
            "test4",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{cls.views[0].pk},new-internal,test1",
            f"{cls.views[1].pk},new-external,test2",
        )

    maxDiff = None
