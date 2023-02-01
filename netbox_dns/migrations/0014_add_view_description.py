from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("netbox_dns", "0012_adjust_zone_and_record"),
        ("netbox_dns", "0013_add_nameserver_zone_record_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="view",
            name="description",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
