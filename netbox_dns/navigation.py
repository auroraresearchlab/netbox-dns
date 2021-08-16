from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_dns:zone_list",
        link_text="Zones",
        buttons=(
            PluginMenuButton(
                "plugins:netbox_dns:zone_add",
                "Zones Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_zone"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dns:nameserver_list",
        link_text="Nameservers",
        buttons=(
            PluginMenuButton(
                "plugins:netbox_dns:nameserver_add",
                "Nameserver Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_nameserver"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dns:record_list",
        link_text="Records",
        buttons=(
            PluginMenuButton(
                "plugins:netbox_dns:record_add",
                "Record Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_record"],
            ),
        ),
    ),
)
