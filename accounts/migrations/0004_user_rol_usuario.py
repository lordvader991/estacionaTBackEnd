# Generated by Django 5.0.3 on 2024-03-26 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20240318_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rol_usuario',
            field=models.BooleanField(default=False),
        ),
    ]
