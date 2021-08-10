from django import template
from django.urls import NoReverseMatch, reverse
from django import template

register = template.Library()


@register.filter()
def plugin_validated_viewname(model, action):
    """Return the view name for :
    * the given model and action if valid
    * or the given model and action if valid inside a plugin
    * or None if invalid.
    """
    core_viewname = f"{model._meta.app_label}:{model._meta.model_name}_{action}"
    plugin_viewname = (
        f"plugins:{model._meta.app_label}:{model._meta.model_name}_{action}"
    )
    try:
        # Validate and return the view name. We don't return the actual URL yet because many of the templates
        # are written to pass a name to {% url %}.
        reverse(core_viewname)
        return core_viewname
    except NoReverseMatch:
        try:
            reverse(plugin_viewname)
            return plugin_viewname
        except NoReverseMatch:
            return None
