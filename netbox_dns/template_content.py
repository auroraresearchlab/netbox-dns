from extras.plugins import PluginTemplateExtension


class RelatedDNSRecords(PluginTemplateExtension):
    model = "ipam.ipaddress"

    def right_page(self):
        return self.render("netbox_dns/related_dns_records.html")


template_extensions = [RelatedDNSRecords]
