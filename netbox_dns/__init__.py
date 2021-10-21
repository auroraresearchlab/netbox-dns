from extras.plugins import PluginConfig

__version__ = "0.5.0"


class DNSConfig(PluginConfig):
    name = "netbox_dns"
    verbose_name = "Netbox DNS"
    description = "Netbox DNS"
    min_version = "3.0.0"
    max_version = None
    version = __version__
    author = "Aurora Research Lab"
    author_email = "info@aurorabilisim.com"
    required_settings = []
    default_settings = {
        "zone": {
            "default_ttl": 86400,
        },
    }


config = DNSConfig
