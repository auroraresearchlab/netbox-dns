# Generated by Django 4.0.3 on 2022-07-28 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netbox_dns", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="record",
            name="status",
            field=models.CharField(default="active", max_length=50),
        ),
    ]