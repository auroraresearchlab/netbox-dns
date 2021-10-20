from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from netbox.models import PrimaryModel, TaggableManager
from utilities.querysets import RestrictedQuerySet
from extras.utils import extras_features


@extras_features("custom_fields", "custom_links", "export_templates", "webhooks")
class NameServer(PrimaryModel):
    name = models.CharField(
        unique=True,
        max_length=255,
    )
    tags = TaggableManager(
        through="extras.TaggedItem",
        blank=True,
    )

    objects = RestrictedQuerySet.as_manager()

    clone_fields = ["name"]

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:nameserver", kwargs={"pk": self.pk})


@extras_features("custom_fields", "custom_links", "export_templates", "webhooks")
class Zone(PrimaryModel):
    STATUS_ACTIVE = "active"
    STATUS_PASSIVE = "passive"

    CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_PASSIVE, "Passive"),
    )

    CSS_CLASSES = {
        STATUS_PASSIVE: "danger",
        STATUS_ACTIVE: "success",
    }

    name = models.CharField(
        unique=True,
        max_length=255,
    )
    status = models.CharField(
        max_length=50,
        choices=CHOICES,
        default=STATUS_ACTIVE,
        blank=True,
    )
    nameservers = models.ManyToManyField(
        NameServer,
        related_name="zones",
        blank=True,
    )
    tags = TaggableManager(
        through="extras.TaggedItem",
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
    soa_serial = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="SOA Serial",
        validators=[MinValueValidator(1), MaxValueValidator(2147483647)],
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

    objects = RestrictedQuerySet.as_manager()

    clone_fields = ["name", "status"]

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:zone", kwargs={"pk": self.pk})

    def get_status_class(self):
        return self.CSS_CLASSES.get(self.status)

    def update_soa_record(self):
        soa_name = "@"
        soa_ttl = self.soa_ttl
        soa_value = (
            f"({self.soa_mname} {self.soa_rname} {self.soa_serial}"
            f" {self.soa_refresh} {self.soa_retry} {self.soa_expire}"
            f" {self.soa_minimum})"
        )

        old_soa_records = Record.objects.filter(
            zone_id=self.id, type=Record.SOA, name=soa_name
        )
        if old_soa_records:
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
                zone_id=self.id,
                type=Record.SOA,
                name=soa_name,
                ttl=soa_ttl,
                value=soa_value,
                managed=True,
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_soa_record()


@extras_features("custom_fields", "custom_links", "export_templates", "webhooks")
class Record(PrimaryModel):
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

    CHOICES = (
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
    )

    zone = models.ForeignKey(
        Zone,
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        choices=CHOICES,
        max_length=10,
    )
    name = models.CharField(
        max_length=255,
    )
    value = models.CharField(
        max_length=1000,
    )
    ttl = models.PositiveIntegerField()
    tags = TaggableManager(
        through="extras.TaggedItem",
        blank=True,
    )
    managed = models.BooleanField(
        null=False,
        default=False,
    )

    objects = RestrictedQuerySet.as_manager()

    clone_fields = ["zone", "type", "name", "value", "ttl"]

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return f"{self.type}:{self.name}"

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:record", kwargs={"pk": self.id})
