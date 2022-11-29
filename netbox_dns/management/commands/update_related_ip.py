from django.core.management.base import BaseCommand

from netbox_dns.models import Record, RecordTypeChoices


class Command(BaseCommand):
    help = "Update the related IP address for all A, AAAA and PTR records"

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose", action="store_true", help="Increase output verbosity"
        )

    def handle(self, *model_names, **options):
        records = Record.objects.filter(type__in=(RecordTypeChoices.A, RecordTypeChoices.AAAA, RecordTypeChoices.PTR), ip_address__isnull=True)

        for record in records:
            if options["verbose"]:
                self.stdout.write(f"Setting the related IP address for record {record}")

            if record.is_address_record:
                record.ip_address = record.value
                record.save()
            else:
                record.ip_address = record.address_from_name
                record.save()

        self.stdout.write(f"All A, AAAA and PTR records have been updated")
