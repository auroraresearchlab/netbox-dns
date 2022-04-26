from django.contrib import admin

from .models import View, Zone, NameServer, Record


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "view", "status")


@admin.register(NameServer)
class NameServerAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("zone", "type", "name", "value", "ttl", "managed")
