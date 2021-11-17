from django.forms import BoundField
from django.urls import reverse

from utilities.forms import DynamicModelMultipleChoiceField


class CustomDynamicModelMultipleChoiceField(DynamicModelMultipleChoiceField):
    def get_bound_field(self, form, field_name):
        bound_field = BoundField(form, self, field_name)

        # Set initial value based on prescribed child fields (if not already set)
        if not self.initial and self.initial_params:
            filter_kwargs = {}
            for kwarg, child_field in self.initial_params.items():
                value = form.initial.get(child_field.lstrip("$"))
                if value:
                    filter_kwargs[kwarg] = value
            if filter_kwargs:
                self.initial = self.queryset.filter(**filter_kwargs).first()

        # Modify the QuerySet of the field before we return it. Limit choices to any data already bound: Options
        # will be populated on-demand via the APISelect widget.
        data = bound_field.value()
        if data:
            field_name = getattr(self, "to_field_name") or "pk"
            filter = self.filter(field_name=field_name)
            try:
                self.queryset = filter.filter(self.queryset, data)
            except (TypeError, ValueError):
                # Catch any error caused by invalid initial data passed from the user
                self.queryset = self.queryset.none()
        else:
            self.queryset = self.queryset.none()

        # Set the data URL on the APISelect widget (if not already set)
        widget = bound_field.field.widget
        if not widget.attrs.get("data-url"):
            app_label = self.queryset.model._meta.app_label
            model_name = self.queryset.model._meta.model_name

            #
            # Custom url for work with plugin api
            #
            data_url = reverse(
                "plugins-api:{}-api:{}-list".format(app_label, model_name)
            )
            widget.attrs["data-url"] = data_url

        return bound_field
