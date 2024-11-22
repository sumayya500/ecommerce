# Generated by Django 5.1.2 on 2024-11-19 07:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cart_shipping_address'),
        ('order', '0007_remove_orderitem_order_remove_payments_order_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Dispatched', 'Dispatched'), ('On the way', 'On the way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Return Request', 'Return Request'), ('Returned', 'Returned')], default='Pending', max_length=20)),
                ('is_paid', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('return_requested', models.BooleanField(default=False)),
                ('return_approved', models.BooleanField(default=False)),
                ('is_refunded', models.BooleanField(default=False)),
                ('payment_method', models.CharField(choices=[('COD', 'Cash on Delivery'), ('STRIPE', 'Stripe')], default='COD', max_length=20)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.address')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Coupons',
        ),
    ]