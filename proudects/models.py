from django.db import models
from ckeditor.fields import RichTextField
from authentication.models import User
# Create your models here.
class Category(models.Model):
    mainCategory = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        )
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    def __str__(self):
        return self.name_ar

class Product(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    old_price = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description_ar = RichTextField()
    description_en = RichTextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        )
    def __str__(self):
        return self.name_ar

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')
    rate = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
    def __str__(self):
        return self.product.name_ar


class color(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='colors')
    color_ar = models.CharField(max_length=100)
    color_en = models.CharField(max_length=100)

    def __str__(self):
        return self.color_ar

class sizes(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='sizes')
    size_ar = models.CharField(max_length=100)
    size_en = models.CharField(max_length=100)
    
    def __str__(self):
        return self.size_ar
    

class Image(models.Model):
    image = models.ImageField(upload_to='products/', default='products/face2028-eb00-4b01-be75-a4fc537a10dc.jpeg')
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return self.product.name_ar
class Banners(models.Model):
    image = models.ImageField(upload_to='banner/')

    def __str__(self) -> str:
        return self.image



