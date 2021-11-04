# Generated by Django 3.2.9 on 2021-11-04 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tenancy", "0002_tenant_ordering"),
        ("netbox_dns", "0002_zone_default_ttl"),
    ]

    operations = [
        migrations.AddField(
            model_name="zone",
            name="auto_renew",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name="zone",
            name="comments",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="zone",
            name="expire_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="zone",
            name="ssl_expire_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="zone",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="zones",
                to="tenancy.tenant",
            ),
        ),
    ]
