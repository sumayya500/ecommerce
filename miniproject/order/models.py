from django.db import models
from django.conf import settings
from product.models import Product 
from cart.models import Cart 
from accounts.models import CustomUser


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='addresses')
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    PIN = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f" {self.name} - {self.address}"
    
class Orders(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    ORDER_STATUS = (
        ("Pending", "Pending"),
        ("Dispatched", "Dispatched"),
        ("On the way", "On the way"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
        ("Return Request", "Return Request"),
        ("Returned", "Returned"),
    )

    status = models.CharField(choices=ORDER_STATUS, default="Pending", max_length=20)
    is_paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    return_requested = models.BooleanField(default=False)
    return_approved = models.BooleanField(default=False)
    is_refunded = models.BooleanField(default=False)  # Track if the order has been refunded

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('STRIPE', 'Stripe'),
    ]
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')


    def __str__(self):
        return f"Order {self.id} for {self.cart.user.email}"


