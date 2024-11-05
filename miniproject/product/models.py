from django.db import models

# Create your models here.
class Category(models.Model):
    Category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.Category_name 
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    desc=models.TextField()
    price=models.FloatField(default=0.0)
    img=models.ImageField(upload_to='products/')
    stock=models.IntegerField(default=0)

    def __str__(self):
            return self.name

