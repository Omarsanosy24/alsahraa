from django.contrib import admin
from rest_framework_api_key.models import APIKey
# Register your models here.
from .models import *
# admin.site.register(APIK`ey)
admin.site.register(order)
admin.site.register(OrderItem)