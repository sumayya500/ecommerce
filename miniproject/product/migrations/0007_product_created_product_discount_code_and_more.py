# Generated by Django 5.1.2 on 2024-11-15 06:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='discount_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
