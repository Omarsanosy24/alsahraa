from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    search_fields = ['username','email','phone']
    list_display = ['username', 'email', 'id', 'created_at','is_verified']
    readonly_fields = ['password']
    # @admin.display(description="mony")
  
admin.site.register(User, UserAdmin)
