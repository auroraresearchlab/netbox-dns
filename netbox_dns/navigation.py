from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_dns:view_list",
        link_text="Views",
        buttons=(
            PluginMenuButton(
                "plugins:netbox_dns:view_add",
                "Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_view"],
            ),
            PluginMenuButton(
                "plugins:netbox_dns:view_import",
                "Import",
                "mdi mdi-upload",
                ButtonColorChoices.CYAN,
                permissions=["netbox_dns.add_view"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dns:zone_list",
        link_text="Zones",
        buttons=(
            PluginMenuButton(
                "plugins:netbox_dns:zone_add",
                "Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_zone"],
            ),
            PluginMenuButton(
                "plugins:netbox_dns:zone_import",
                "Import",
                "mdi mdi-upload",
                ButtonColorChoices.CYAN,
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
                "Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_nameserver"],
            ),
            PluginMenuButton(
                "plugins:netbox_dns:nameserver_import",
                "Import",
                "mdi mdi-upload",
                ButtonColorChoices.CYAN,
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
                "Add",
                "mdi mdi-plus-thick",
                ButtonColorChoices.GREEN,
                permissions=["netbox_dns.add_record"],
            ),
            PluginMenuButton(
                "plugins:netbox_dns:record_import",
                "Import",
                "mdi mdi-upload",
                ButtonColorChoices.CYAN,
                permissions=["netbox_dns.add_record"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_dns:managed_record_list",
        link_text="Managed Records",
    ),
)
