# Generated by Django 5.0.3 on 2024-04-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parqueo', '0009_price_is_entry_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricehour',
            name='end_time',
            field=models.TimeField(default=None),
        ),
        migrations.AlterField(
            model_name='pricehour',
            name='start_time',
            field=models.TimeField(default=None),
        ),
    ]
