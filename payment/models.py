from django.db import models
from authentication.models import User
from proudects.models import *
# Create your models here.
class order(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    note = models.TextField(blank=True,null=True)
    state = models.TextField(null=True,blank=True)
    homeDes = models.TextField(blank=True,null=True)
    country = models.TextField(null=True,blank=True)
    phone = models.CharField(max_length=20)
    auth_key = models.TextField(blank=True, null=True)
    status = models.CharField(null=True, blank=True, max_length=20)
    def __str__(self) -> str:
        return self.user.username
    # def save(self,*args, **kwargs):
        

    @property
    def total_price(self):
        return sum(self.items.values_list('price',flat=True))
class OrderItem(models.Model):
    order = models.ForeignKey(order,on_delete=models.CASCADE,related_name='items')
    product = models.CharField(max_length=150)
    size = models.CharField(max_length=50,null=True,blank=True)
    color = models.CharField(max_length=50,null=True,blank=True)
    quantity = models.PositiveSmallIntegerField()
    price = models.FloatField()

    

    