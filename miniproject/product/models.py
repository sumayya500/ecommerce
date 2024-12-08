from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    categoryname = models.CharField(max_length=200)

    def __str__(self):
        return self.categoryname 
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    desc=models.TextField()
    price=models.FloatField(default=0.0)
    discount_percentage = models.FloatField(null=True,blank=True)  # Discount in percentage (e.g., 20 for 20%)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Optional discount price
    img=models.ImageField(upload_to='products/')
    stock=models.IntegerField(default=0)


    def get_discounted_price(self):
        """
        Returns the price after applying the discount.
        If both `discount_percentage` and `discount_price` are set, priority is given to `discount_price`.
        """
        if self.discount_price:
            return self.discount_price
        elif self.discount_percentage and self.discount_percentage > 0:
            return self.price - (self.price * self.discount_percentage / 100)
        return self.price

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically calculate the discount_price
        based on the discount_percentage before saving the product.
        """
        if self.discount_percentage and self.discount_percentage > 0:
            self.discount_price = round(self.price - (self.price * self.discount_percentage / 100), 2)
        else:
            self.discount_price = None  # Reset if no valid discount is set
        super().save(*args, **kwargs)


    def __str__(self):
            return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL here
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link the wishlist to a product
    added_on = models.DateTimeField(auto_now_add=True)

class Meta:
        unique_together = ('user', 'product')  # Prevent adding the same product twice to the same user's wishlist
def __str__(self):
        return f"{self.user.username} - {self.product.name}"