# Generated by Django 5.1.2 on 2024-11-16 08:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_address_alter_order_address_delete_addresss'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('min_amount', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Coupon',
                'verbose_name_plural': 'Coupons',
                'db_table': 'Coupons',
            },
        ),
    ]
