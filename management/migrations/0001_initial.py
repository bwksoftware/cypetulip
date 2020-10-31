# Generated by Django 2.2.4 on 2019-08-11 11:10

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MailSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_server', models.CharField(max_length=100)),
                ('smtp_port', models.IntegerField()),
                ('smtp_user', models.CharField(max_length=100)),
                ('smtp_password', models.CharField(max_length=100)),
                ('stmp_use_tls', models.BooleanField(max_length=100)),
                ('smtp_default_from', models.CharField(max_length=100)),
            ],
        ),
    ]