# Generated by Django 5.2 on 2025-04-24 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
