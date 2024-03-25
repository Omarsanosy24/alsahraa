from django.contrib import admin
from .models import *
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import ForeignKey
from copy import deepcopy
# Register your models here.
def duplicate_selected_products(modeladmin, request, queryset):
    # Iterate over the selected products and create a copy of each one
    for obj in queryset:
        # Create a deepcopy of the object to include all related fields
        obj_copy = deepcopy(obj)
        # Set the ID to None so that a new object is created
        obj_copy.id = None
        # Set a new name for the duplicated product
        obj_copy.name_ar += ' (Copy)'
        # Save the duplicated product
        obj_copy.save()

        # Duplicate the related many-to-many fields
        for image in obj.images.all():
                image.pk = None
                image =image.copy()
                image.product = obj_copy
                image.save()
        for size in obj.sizes.all():
                size.pk = None
                size = size.copy()
                size.products = obj_copy
                size.save()
        for color in obj.colors.all():
                color.pk = None
                color = color.copy()
                color.products = obj_copy
                color.save()

    # Display a success message to the user
    modeladmin.message_user(request, ('The selected products have been duplicated.'))
duplicate_selected_products.short_description = _('Duplicate selected products')
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
    actions = [duplicate_selected_products]
admin.site.register(Tags)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Banners)
admin.site.register(Rate)
admin.site.register(MainCategory)
admin.site.register(commitForWeb)
admin.site.register(Links)
admin.site.register(MediaModel)