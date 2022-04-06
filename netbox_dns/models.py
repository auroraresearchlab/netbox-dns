import ipaddress

from math import ceil
from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models import Q, Max, ExpressionWrapper, BooleanField
from django.db.models.functions import Length
from django.urls import reverse

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from utilities.choices import ChoiceSet


def absolute_name(name):
    if name.endswith("."):
        return name
    return f"{name}."


class NameServer(NetBoxModel):
    name = models.CharField(
        unique=True,
        max_length=255,
    )

    clone_fields = ["name"]

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:nameserver", kwargs={"pk": self.pk})


class ZoneManager(models.Manager.from_queryset(RestrictedQuerySet)):
    """Special Manager for zones providing the activity status annotation"""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                active=ExpressionWrapper(
                    Q(status__in=Zone.ACTIVE_STATUS_LIST), output_field=BooleanField()
                )
            )
        )


class ZoneStatusChoices(ChoiceSet):
    key = "Zone.status"

    STATUS_ACTIVE = "active"
    STATUS_RESERVED = "reserved"
    STATUS_DEPRECATED = "deprecated"
    STATUS_PARKED = "parked"

    CHOICES = [
        (STATUS_ACTIVE, "Active", "blue"),
        (STATUS_RESERVED, "Reserved", "cyan"),
        (STATUS_DEPRECATED, "Deprecated", "red"),
        (STATUS_PARKED, "Parked", "gray"),
    ]


class Zone(NetBoxModel):
    ACTIVE_STATUS_LIST = (ZoneStatusChoices.STATUS_ACTIVE,)

    name = models.CharField(
        unique=True,
        max_length=255,
    )
    status = models.CharField(
        max_length=50,
        choices=ZoneStatusChoices,
        default=ZoneStatusChoices.STATUS_ACTIVE,
        blank=True,
    )
    nameservers = models.ManyToManyField(
        NameServer,
        related_name="zones",
        blank=True,
    )
    default_ttl = models.PositiveIntegerField(
        blank=True,
        verbose_name="Default TTL",
        validators=[MinValueValidator(1)],
    )
    soa_ttl = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="SOA TTL",
        validators=[MinValueValidator(1)],
    )
    soa_mname = models.ForeignKey(
        NameServer,
        related_name="zones_soa",
        verbose_name="SOA MName",
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )
    soa_rname = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="SOA RName",
    )
    soa_serial = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="SOA Serial",
        validators=[MinValueValidator(1), MaxValueValidator(4294967295)],
    )
    soa_refresh = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="SOA Refresh",
        validators=[MinValueValidator(1)],
    )
    soa_retry = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="SOA Retry",
        validators=[MinValueValidator(1)],
    )
    soa_expire = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="SOA Expire",
        validators=[MinValueValidator(1)],
    )
    soa_minimum = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="SOA Minimum TTL",
        validators=[MinValueValidator(1)],
    )
    soa_serial_auto = models.BooleanField(
        verbose_name="Generate SOA Serial",
        help_text="Automatically generate the SOA Serial field",
        default=True,
    )

    objects = ZoneManager()

    clone_fields = [
        "name",
        "status",
        "nameservers",
        "default_ttl",
        "soa_ttl",
        "soa_mname",
        "soa_rname",
        "soa_refresh",
        "soa_retry",
        "soa_expire",
        "soa_minimum",
    ]

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return str(self.name)

    def get_status_color(self):
        return ZoneStatusChoices.colors.get(self.status)

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:zone", kwargs={"pk": self.pk})

    def get_status_class(self):
        return self.CSS_CLASSES.get(self.status)

    def update_soa_record(self):
        soa_name = "@"
        soa_ttl = self.soa_ttl
        soa_value = (
            f"({absolute_name(self.soa_mname.name)} {absolute_name(self.soa_rname)}"
            f" {self.soa_serial}"
            f" {self.soa_refresh} {self.soa_retry} {self.soa_expire}"
            f" {self.soa_minimum})"
        )

        old_soa_records = self.record_set.filter(
            type=RecordTypeChoices.SOA, name=soa_name
        )

        if len(old_soa_records):
            for index, record in enumerate(old_soa_records):
                if index > 0:
                    record.delete()
                    continue

                if record.ttl != soa_ttl or record.value != soa_value:
                    record.ttl = soa_ttl
                    record.value = soa_value
                    record.managed = True
                    record.save()
        else:
            Record.objects.create(
                zone_id=self.pk,
                type=RecordTypeChoices.SOA,
                name=soa_name,
                ttl=soa_ttl,
                value=soa_value,
                managed=True,
            )

    def update_ns_records(self, nameservers):
        ns_name = "@"
        ns_ttl = self.default_ttl

        delete_ns = self.record_set.filter(
            type=RecordTypeChoices.NS, managed=True
        ).exclude(value__in=nameservers)
        for record in delete_ns:
            record.delete()

        for ns in nameservers:
            Record.raw_objects.update_or_create(
                zone_id=self.pk,
                type=RecordTypeChoices.NS,
                name=ns_name,
                ttl=ns_ttl,
                value=ns,
                managed=True,
            )

    def check_nameservers(self):
        nameservers = self.nameservers.all()

        ns_warnings = []
        ns_errors = []

        if not nameservers:
            ns_errors.append(f"No nameservers are configured for zone {self.name}")

        for nameserver in nameservers:
            ns_domain = ".".join(nameserver.name.split(".")[1:])
            if not ns_domain:
                continue

            try:
                ns_zone = Zone.objects.get(name=ns_domain)
            except ObjectDoesNotExist:
                continue

            ns_name = nameserver.name.split(".")[0]
            address_records = Record.objects.filter(
                Q(zone=ns_zone),
                Q(Q(name=f"{nameserver.name}.") | Q(name=ns_name)),
                Q(Q(type=RecordTypeChoices.A) | Q(type=RecordTypeChoices.AAAA)),
            )

            if not address_records:
                ns_warnings.append(
                    f"Nameserver {nameserver.name} does not have an address record in zone {ns_zone.name}"
                )

        return ns_warnings, ns_errors

    def get_auto_serial(self):
        records = Record.objects.filter(zone=self).exclude(type=RecordTypeChoices.SOA)
        if records:
            soa_serial = (
                records.aggregate(Max("last_updated"))
                .get("last_updated__max")
                .timestamp()
            )
        else:
            soa_serial = ceil(datetime.now().timestamp())

        if self.last_updated:
            soa_serial = ceil(max(soa_serial, self.last_updated.timestamp()))

        return soa_serial

    def update_serial(self):
        self.last_updated = datetime.now()
        self.save()

    def parent_zones(self):
        zone_fields = self.name.split(".")
        return [
            f'{".".join(zone_fields[length:])}' for length in range(1, len(zone_fields))
        ]

    def save(self, *args, **kwargs):
        new_zone = self.pk is None
        if not new_zone:
            renamed_zone = Zone.objects.get(pk=self.pk).name != self.name
        else:
            renamed_zone = False

        if self.soa_serial_auto:
            self.soa_serial = self.get_auto_serial()

        super().save(*args, **kwargs)

        if (new_zone or renamed_zone) and self.name.endswith(".arpa"):
            address_records = Record.objects.filter(
                Q(ptr_record__isnull=True)
                | Q(ptr_record__zone__name__in=self.parent_zones()),
                type__in=(RecordTypeChoices.A, RecordTypeChoices.AAAA),
                disable_ptr=False,
            )
            for record in address_records:
                record.update_ptr_record()

        elif renamed_zone:
            for record in self.record_set.filter(ptr_record__isnull=False):
                record.update_ptr_record()

        self.update_soa_record()

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            address_records = list(self.record_set.filter(ptr_record__isnull=False))
            for record in address_records:
                record.ptr_record.delete()

            ptr_records = self.record_set.filter(address_record__isnull=False)
            update_records = [
                record.pk
                for record in Record.objects.filter(ptr_record__in=ptr_records)
            ]

            super().delete(*args, **kwargs)

        for record in Record.objects.filter(pk__in=update_records):
            record.update_ptr_record()


@receiver(m2m_changed, sender=Zone.nameservers.through)
def update_ns_records(**kwargs):
    if kwargs.get("action") not in ["post_add", "post_remove"]:
        return

    zone = kwargs.get("instance")
    nameservers = zone.nameservers.all()

    new_nameservers = [f'{ns.name.rstrip(".")}.' for ns in nameservers]

    zone.update_ns_records(new_nameservers)


class RecordManager(models.Manager.from_queryset(RestrictedQuerySet)):
    """Special Manager for records providing the activity status annotation"""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                active=ExpressionWrapper(
                    Q(
                        Q(zone__status__in=Zone.ACTIVE_STATUS_LIST)
                        & Q(
                            Q(address_record__isnull=True)
                            | Q(
                                address_record__zone__status__in=Zone.ACTIVE_STATUS_LIST
                            )
                        )
                    ),
                    output_field=BooleanField(),
                )
            )
        )


class RecordTypeChoices(ChoiceSet):
    key = "Record.type"

    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    TXT = "TXT"
    NS = "NS"
    SOA = "SOA"
    SRV = "SRV"
    PTR = "PTR"
    SPF = "SPF"
    CAA = "CAA"
    DS = "DS"
    SSHFP = "SSHFP"
    TLSA = "TLSA"
    AFSDB = "AFSDB"
    APL = "APL"
    DNSKEY = "DNSKEY"
    CDNSKEY = "CDNSKEY"
    CERT = "CERT"
    DCHID = "DCHID"
    DNAME = "DNAME"
    HIP = "HIP"
    IPSECKEY = "IPSECKEY"
    LOC = "LOC"
    NAPTR = "NAPTR"
    NSEC = "NSEC"
    RRSIG = "RRSIG"
    RP = "RP"

    CHOICES = [
        (A, A),
        (AAAA, AAAA),
        (CNAME, CNAME),
        (MX, MX),
        (TXT, TXT),
        (SOA, SOA),
        (NS, NS),
        (SRV, SRV),
        (PTR, PTR),
        (SPF, SPF),
        (CAA, CAA),
        (DS, DS),
        (SSHFP, SSHFP),
        (TLSA, TLSA),
        (AFSDB, AFSDB),
        (APL, APL),
        (DNSKEY, DNSKEY),
        (CDNSKEY, CDNSKEY),
        (CERT, CERT),
        (DCHID, DCHID),
        (DNAME, DNAME),
        (HIP, HIP),
        (IPSECKEY, IPSECKEY),
        (LOC, LOC),
        (NAPTR, NAPTR),
        (NSEC, NSEC),
        (RRSIG, RRSIG),
        (RP, RP),
    ]


class Record(NetBoxModel):
    unique_ptr_qs = Q(
        Q(disable_ptr=False),
        Q(Q(type=RecordTypeChoices.A) | Q(type=RecordTypeChoices.AAAA)),
    )

    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        choices=RecordTypeChoices,
        max_length=10,
    )
    name = models.CharField(
        max_length=255,
    )
    value = models.CharField(
        max_length=1000,
    )
    ttl = models.PositiveIntegerField(
        verbose_name="TTL",
    )
    managed = models.BooleanField(
        null=False,
        default=False,
    )
    ptr_record = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        related_name="address_record",
        verbose_name="PTR record",
        null=True,
        blank=True,
    )
    disable_ptr = models.BooleanField(
        verbose_name="Disable PTR",
        help_text="Disable PTR record creation",
        default=False,
    )

    objects = RecordManager()
    raw_objects = RestrictedQuerySet.as_manager()

    clone_fields = ["zone", "type", "name", "value", "ttl", "disable_ptr"]

    class Meta:
        ordering = ("zone", "name", "type", "value")
        constraints = (
            models.UniqueConstraint(
                name="unique_pointer_for_address",
                fields=["type", "value"],
                condition=(
                    models.Q(
                        models.Q(disable_ptr=False),
                        models.Q(type=RecordTypeChoices.A)
                        | models.Q(type=RecordTypeChoices.AAAA),
                    )
                ),
            ),
        )

    def __str__(self):
        if self.name == "@":
            return f"{self.zone.name} [{self.type}]"

        if self.name.endswith("."):
            return f"{self.name} [{self.type}]"

        return f"{self.name}.{self.zone.name} [{self.type}]"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:record", kwargs={"pk": self.id})

    def fqdn(self):
        return f"{self.name}.{self.zone.name}."

    def ptr_zone(self):
        address = ipaddress.ip_address(self.value)
        if address.version == 4:
            lengths = range(1, 4)
        else:
            lengths = range(16, 32)

        zone_names = [
            ".".join(address.reverse_pointer.split(".")[length:]) for length in lengths
        ]

        ptr_zones = Zone.objects.filter(Q(name__in=zone_names)).order_by(
            Length("name").desc()
        )
        if len(ptr_zones):
            return ptr_zones[0]

        return None

    def update_ptr_record(self):
        ptr_zone = self.ptr_zone()

        if ptr_zone is None or self.disable_ptr:
            if self.ptr_record is not None:
                with transaction.atomic():
                    self.ptr_record.delete()
                    self.ptr_record = None
            return

        ptr_name = ipaddress.ip_address(self.value).reverse_pointer.replace(
            f".{ptr_zone.name}", ""
        )
        ptr_value = self.fqdn()
        ptr_record = self.ptr_record

        with transaction.atomic():
            if ptr_record is not None:
                if ptr_record.zone.pk != ptr_zone.pk:
                    ptr_record.delete()
                    ptr_record = None

                else:
                    if (
                        ptr_record.name != ptr_name
                        or ptr_record.value != ptr_value
                        or ptr_record.ttl != self.ttl
                    ):
                        ptr_record.name = ptr_name
                        ptr_record.value = ptr_value
                        ptr_record.ttl = self.ttl
                        ptr_record.save()

            if ptr_record is None:
                ptr_record = Record.objects.create(
                    zone_id=ptr_zone.pk,
                    type=RecordTypeChoices.PTR,
                    name=ptr_name,
                    ttl=self.ttl,
                    value=ptr_value,
                    managed=True,
                )

        self.ptr_record = ptr_record
        super().save()

    def save(self, *args, **kwargs):
        if self.type in (RecordTypeChoices.A, RecordTypeChoices.AAAA):
            self.update_ptr_record()

        super().save(*args, **kwargs)

        zone = self.zone
        if self.type != RecordTypeChoices.SOA and zone.soa_serial_auto:
            zone.update_serial()

    def delete(self, *args, **kwargs):
        if self.ptr_record:
            self.ptr_record.delete()

        super().delete(*args, **kwargs)

        zone = self.zone
        if zone.soa_serial_auto:
            zone.update_serial()
