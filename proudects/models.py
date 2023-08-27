import random
from typing import Iterable, Optional
from django.db import models
from ckeditor.fields import RichTextField
from authentication.models import User
# Create your models here.
from django.core.exceptions import ValidationError
from django.db.models import Count

class MainCategory(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    def __str__(self):
        return self.name_ar

class Category(models.Model):
    mainCategory = models.ForeignKey(
        MainCategory,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="mainCate"
        )
    subCategory = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subCate"
        )
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    def __str__(self):
        return self.name_ar
    def clean(self):
        if self.mainCategory and self.subCategory:
            raise ValidationError('You can only select one category')
        elif not self.mainCategory and not self.subCategory:
            raise ValidationError("Please choose a category")
class Tags(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    def __str__(self) -> str:
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
        related_name='products'
        )
    star = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True, related_name='tag')
    wishlist = models.ManyToManyField(User,blank=True , related_name='wish')
    text_on_photo_ar = models.TextField( null=True, blank=True)
    text_on_photo_en = models.TextField( null=True, blank=True)

    PendingOrders = models.ManyToManyField(User,blank=True , related_name='PendingOrder')


    def __str__(self):
        return self.name_ar
    
    
    
    
class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rates')
    comment = models.TextField(null=True, blank=True)
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
    def copy(self):
        # Create a new instance of the model with all the same attributes
        obj = self.__class__.objects.create(
            products=self.products,
            color_ar=f"Copy of {self.color_ar}",
            color_en=f"Copy of {self.color_en}",

        )
        return obj
class sizes(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='sizes')
    size_ar = models.CharField(max_length=100)
    size_en = models.CharField(max_length=100)
    
    def __str__(self):
        return self.size_ar
    def copy(self):
        # Create a new instance of the model with all the same attributes
        obj = self.__class__.objects.create(
            products=self.products,
            size_ar=f"Copy of {self.size_ar}",
            size_en=f"Copy of {self.size_en}",

        )
        return obj

class Image(models.Model):
    image = models.ImageField(upload_to='products/', default='products/face2028-eb00-4b01-be75-a4fc537a10dc.jpeg')
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name='images')

    def __str__(self) -> str:
        return self.product.name_ar
    def copy(self):
        # Create a new instance of the model with all the same attributes
        obj = self.__class__.objects.create(
            product=self.product,
            image=self.image,
        )
        return obj
class Banners(models.Model):
    choices = [
        ('fr','first'),
        ('sc','second'),
        ('th','third'),
    ]
    image = models.ImageField(upload_to='banner/')
    place = models.CharField(choices=choices, max_length=8, default='first')
    def __str__(self) -> str:
        return self.place
    


class Links(models.Model):
    choices = [
        ('phone','phone'),
        ('mobile','mobile'),
        ('whatsapp','whatsapp'),
        ('telegram','telegram'),
        ('email','email'),
        ('youtube','youtube'),
        ("tiktok","tiktok"),
        ('snap','snap'),
        ('insta',"insta"),
        ('facebook',"facebook"),
        ('twitter',"twitter"),
    ]
    kind = models.CharField(choices=choices, max_length=20, unique=True)
    value = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.kind
    

class MediaModel(models.Model):
    url = models.TextField()
    image = models.ImageField(upload_to='mediaModel/')

    def __str__(self) -> str:
        return self.url