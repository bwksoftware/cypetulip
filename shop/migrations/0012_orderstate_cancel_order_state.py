# Generated by Django 3.0.2 on 2020-02-02 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0011_auto_20200202_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderstate',
            name='cancel_order_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='cancel_state', to='shop.OrderState'),
        ),
    ]