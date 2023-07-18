from django.contrib import admin
from .models import *
# Register your models here.

class ImageAdmin(admin.StackedInline):
    model = Image
    extra = 3
class colorAdmin(admin.StackedInline):
    model = color
    extra = 2
class sizesAdmin(admin.StackedInline):
    model = sizes
    extra = 2
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageAdmin,sizesAdmin,colorAdmin]


admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Banners)
