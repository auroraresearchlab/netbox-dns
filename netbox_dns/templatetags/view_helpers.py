from django import template
from django.urls import NoReverseMatch, reverse
from django import template

from utilities.templatetags.buttons import _get_viewname
from utilities.utils import prepare_cloned_fields

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


@register.filter()
def plugin_viewname(model, action):
    """
    Return the view name for the given model and action. Does not perform any validation.
    """
    return f"plugins:{model._meta.app_label}:{model._meta.model_name}_{action}"


#
# Instance buttons
#


@register.inclusion_tag("buttons/clone.html")
def plugin_clone_button(instance):
    viewname = _get_viewname(instance, "add")
    url = reverse(f"plugins:{viewname}")

    # Populate cloned field values
    param_string = prepare_cloned_fields(instance)
    if param_string:
        url = f"{url}?{param_string}"

    return {
        "url": url,
    }


@register.inclusion_tag("buttons/edit.html")
def plugin_edit_button(instance, **kwargs):
    viewname = _get_viewname(instance, "edit")
    url = reverse(f"plugins:{viewname}", kwargs={"pk": instance.pk, **kwargs})

    return {
        "url": url,
    }


@register.inclusion_tag("buttons/delete.html")
def plugin_delete_button(instance, **kwargs):
    viewname = _get_viewname(instance, "delete")
    url = reverse(f"plugins:{viewname}", kwargs={"pk": instance.pk, **kwargs})

    return {
        "url": url,
    }


#
# List buttons
#


@register.inclusion_tag("buttons/add.html")
def plugin_add_button(url):
    url = reverse(f"plugins:{url}")

    return {
        "add_url": url,
    }
