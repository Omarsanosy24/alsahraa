from rest_framework import serializers
from .models import *


class CategorySerializers(serializers.ModelSerializer):
    mainCategory = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_mainCategory(self,obj):
        if obj.mainCategory:
            return CategorySerializers(obj.mainCategory).data
        return None

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class sizesSerializers(serializers.ModelSerializer):
    class Meta:
        model = sizes
        fields = '__all__'
class colorSerializers(serializers.ModelSerializer):
    class Meta:
        model = color
        fields = '__all__'



class ProductsSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    images = ImageSerializers(many=True)
    colors = colorSerializers(many=True)
    sizes = sizesSerializers(many=True)

    class Meta:
        model = Product
        fields = '__all__'

class BannersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Banners
        fields = '__all__'