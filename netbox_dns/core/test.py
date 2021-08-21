from django.urls import reverse

from utilities.testing.views import ModelViewTestCase as NetBoxModelViewTestCase


class ModelViewTestCase(NetBoxModelViewTestCase):
    """
    Customize viewtestcase for work with plugins

    Base TestCase for model views. Subclass to test individual views.
    """

    def _get_base_url(self):
        """
        Return the base format for a URL for the test's model. Override this to test for a model which belongs
        to a different app (e.g. testing Interfaces within the virtualization app).
        """
        return "plugins:{}:{}_{{}}".format(
            self.model._meta.app_label, self.model._meta.model_name
        )

    def _get_url(self, action, instance=None):
        """
        Return the URL name for a specific action and optionally a specific instance
        """
        url_format = self._get_base_url()

        # If no instance was provided, assume we don't need a unique identifier
        if instance is None:
            return reverse(url_format.format(action))

        return reverse(url_format.format(action), kwargs={"pk": instance.pk})
