# Generated by Django 3.0.2 on 2020-05-15 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shipping', '0001_initial'),
        ('shop', '0019_auto_20200515_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='shipment', to='shipping.Shipment'),
        ),
    ]
