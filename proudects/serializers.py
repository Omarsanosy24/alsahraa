from rest_framework import serializers
from .models import *
class MainCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = MainCategory
        fields = '__all__'

class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductsSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class BannersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Banners
        fields = '__all__'