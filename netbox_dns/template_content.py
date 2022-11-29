from extras.plugins import PluginTemplateExtension

from netbox_dns.models import Record, RecordTypeChoices
from netbox_dns.tables import RelatedRecordTable


class RelatedDNSRecords(PluginTemplateExtension):
    model = "ipam.ipaddress"

    def right_page(self):
        obj = self.context.get("object")

        address_records = Record.objects.filter(
            ip_address=obj.address.ip,
            type__in=(RecordTypeChoices.A, RecordTypeChoices.AAAA),
        )
        pointer_records = Record.objects.filter(
            ip_address=obj.address.ip, type=RecordTypeChoices.PTR
        )
        address_record_table = RelatedRecordTable(
            data=address_records,
        )
        pointer_record_table = RelatedRecordTable(
            data=pointer_records,
        )

        return self.render(
            "netbox_dns/record/related.html",
            extra_context={
                "related_address_records": address_record_table,
                "related_pointer_records": pointer_record_table,
            },
        )


template_extensions = [RelatedDNSRecords]
