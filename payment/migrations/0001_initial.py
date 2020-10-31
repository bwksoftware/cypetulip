# Generated by Django 3.0.2 on 2020-05-11 13:35

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0016_auto_20200511_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=40)),
                ('secret', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('paymentdetail_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='payment.PaymentDetail')),
            ],
            bases=('payment.paymentdetail',),
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('details', models.CharField(default='', max_length=500)),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='payment.PaymentProvider')),
            ],
        ),
        migrations.AddField(
            model_name='paymentdetail',
            name='method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='paymentdetail',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Order'),
        ),
        migrations.AddField(
            model_name='paymentdetail',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Contact'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField()),
                ('token', models.CharField(max_length=30)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.PaymentDetail')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('paymentdetail_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='payment.PaymentDetail')),
                ('name', models.CharField(max_length=70)),
                ('card_number', models.CharField(max_length=20)),
                ('expiry_year', models.IntegerField(
                    choices=[(2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025),
                             (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030)], default=2020)),
                ('expiry_month', models.IntegerField(
                    choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11),
                             (12, 12)], default=5)),
                ('cvv', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(999)])),
                ('card_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.CardType')),
            ],
            bases=('payment.paymentdetail',),
        ),
    ]