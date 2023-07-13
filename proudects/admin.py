from django.contrib import admin
from .models import *
# Register your models here.

class ImageAdmin(admin.StackedInline):
    model = Image
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin]


admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Banners)
