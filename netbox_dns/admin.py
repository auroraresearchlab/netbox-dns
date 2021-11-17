from django.contrib import admin

from .models import Zone, NameServer, Record


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "status")


@admin.register(NameServer)
class NameServerAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("zone", "type", "name", "value", "ttl", "managed")
