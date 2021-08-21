from django.db import models
from django.urls import reverse
from netbox.models import PrimaryModel, TaggableManager
from utilities.querysets import RestrictedQuerySet


class NameServer(PrimaryModel):
    name = models.CharField(unique=True, max_length=255)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:nameserver", kwargs={"pk": self.pk})


class Zone(PrimaryModel):
    STATUS_ACTIVE = "active"
    STATUS_PASSIVE = "passive"

    CHOICES = (
        (STATUS_ACTIVE, "Active"),
        (STATUS_PASSIVE, "Passive"),
    )

    name = models.CharField(unique=True, max_length=255)
    status = models.CharField(
        max_length=50, choices=CHOICES, default=STATUS_ACTIVE, blank=True
    )
    nameservers = models.ManyToManyField(NameServer, related_name="zones", blank=True)
    tags = TaggableManager(through="extras.TaggedItem", blank=True)

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_dns:zone", kwargs={"pk": self.pk})


class Record(PrimaryModel):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    TXT = "TXT"
    NS = "NS"

    CHOICES = ((A, A), (AAAA, AAAA), (CNAME, CNAME), (MX, MX), (TXT, TXT), (NS, NS))

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    type = models.CharField(choices=CHOICES, max_length=10)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=1000)
    ttl = models.PositiveIntegerField()

    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ("name", "id")

    def __str__(self):
        return f"{self.type}:{self.name}"

    def get_absolute_url(self):
        """
        Redirect corresponding zone url.
        """
        return reverse("plugins:netbox_dns:record", kwargs={"pk": self.id})
