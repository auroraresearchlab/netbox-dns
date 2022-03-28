from pkg_resources import parse_version
from django.conf import settings
from django import template

register = template.Library()


#
# Version check
#


@register.filter()
def check_version(version):
    return parse_version(settings.VERSION) < parse_version(version)
