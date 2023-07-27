from rest_framework import serializers
from .models import *
from authentication.serializers import UserSer

class CatWithProSerializers(serializers.ModelSerializer):
    pass 

class CategorySerializers(serializers.ModelSerializer):
    subCategory = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
    
    def get_subCategory(self,obj):
        if obj.subCate:
            query = obj.subCate.all()
            return CategorySerializers(query,many=True).data
        return None
class MainCategorySerializers(serializers.ModelSerializer):
    subCate = CategorySerializers(source = 'mainCate', many=True, read_only=True)
    class Meta:
        model = MainCategory
        fields = '__all__'
class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        # read_only_fields = ['id','product']

class sizesSerializers(serializers.ModelSerializer):
    class Meta:
        model = sizes
        fields = '__all__'
        read_only_fields = ['id','products']
        
class colorSerializers(serializers.ModelSerializer):
    class Meta:
        model = color
        fields = '__all__'
        read_only_fields = ['id','products']
class tagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
        read_only_fields = ['name_ar','name_en']
class RateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.CharField(source='user.username',read_only=True)
    image = serializers.ImageField(source = 'user.image',read_only=True)
    class Meta:
        model = Rate
        fields = '__all__'
        
class ProductsSerializers(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    category_patch = serializers.IntegerField(write_only=True)
    images = ImageSerializers(many=True,read_only=True)
    colors = colorSerializers(many=True)
    sizes = sizesSerializers(many=True)
    rateNum = serializers.SerializerMethodField(read_only=True)
    rates = RateSerializers(many=True, read_only=True)
    wish = serializers.SerializerMethodField()
    tags = tagsSerializers(read_only=True, many=True)
    class Meta:
        model = Product
        fields = [
            'id','category',
            'images', 'colors',
            'sizes','rateNum',
            'rates','wish',
            'name_ar','name_en',
            'old_price','price',
            'star','tags',
            'description_ar',
            'description_en',
            'category_patch',
            'text_on_photo'
            ]
        read_only_fields = ['wishlist']

    def get_rateNum(self, obj):
        values = Rate.objects.filter(product = obj).values_list('rate',flat=True)
        try:
            return sum(values)/len(values)
        except:
            return None
    def get_wish(self,obj):
        user = self.context['request'].user
        if user:
            if user in obj.wishlist.all():
                return True
        return False
    # def get_tags(self,obj):
    #     if obj.tag:
    #         return(tagsSerializers(obj.tag).data)
    def update(self, instance, validated_data):
        colors_data = validated_data.pop('colors', None)
        sizes_data = validated_data.pop('sizes', None)
        cat = validated_data.pop('category_patch',None)
        if colors_data:
            instance.colors.all().delete()
            for color in colors_data:
                color_id = color.pop('id', None)
                if color_id:
                    color_inst = instance.colors.filter(id=color_id).first()
                    color_inst.color_ar = color.get('color_ar', color_inst.color_ar)
                    color_inst.color_en = color.get('color_en', color_inst.color_en)
                    color_inst.save()
                else:
                    instance.colors.create(color_ar=color['color_ar'], color_en=color["color_en"])
        if cat:
            instance.category = Category.objects.get(id=cat)
            instance.save()
        if sizes_data:
            instance.sizes.all().delete()
            for color in sizes_data:
                instance.sizes.create(size_ar=color['size_ar'], size_en=color["size_en"])
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        colors_data = validated_data.pop('colors', None)
        sizes_data = validated_data.pop('sizes', None)
        images = validated_data('images',None)
        cat = validated_data.pop('category_patch')
        name_ar = validated_data.pop('name_ar')
        name_en = validated_data.pop('name_en')
        price = validated_data.pop('price')
        old_price = validated_data.pop('old_price',None)
        description_ar = validated_data.pop('description_ar')
        description_en = validated_data.pop('description_en')
        instance = Product(
            category = Category.objects.get(id=cat),
            name_ar=name_ar,
            name_en=name_en,
            price=price,
            old_price=old_price,
            description_ar=description_ar,
            description_en=description_en,
            )
        instance.save()
        if colors_data:
            for color in colors_data:
                instance.colors.create(color_ar=color['color_ar'], color_en=color["color_en"])
        if sizes_data:
            for color in sizes_data:
                instance.sizes.create(size_ar=color['size_ar'], size_en=color["size_en"])
        if images:
            for image in images:
                instance.images.create(image=image['image'])
        return instance



class BannersSerializers(serializers.ModelSerializer):

    class Meta:
        model = Banners
        fields = '__all__'

class AddToWishListSer(serializers.Serializer):
    id_product = serializers.IntegerField(write_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        id_product = validated_data.pop('id_product')
        try:
            instance = Product.objects.get(id=id_product)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"id_product":"Product with id {} does not exist".format(id_product)})
        user = self.context['request'].user
        if user in instance.wishlist.all():
            instance.wishlist.remove(user)
            return {"message":"تمت الازالة من المفضلة"}
        else:
            instance.wishlist.add(user)
            return {"message":"تمت الاضافة من المفضلة"}
    
class PendingOrdersSer(serializers.Serializer):
    id_product = serializers.IntegerField(write_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        id_product = validated_data.pop('id_product')
        try:
            instance = Product.objects.get(id=id_product)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"id_product":"Product with id {} does not exist".format(id_product)})
        user = self.context['request'].user
        if user in instance.PendingOrder.all():
            instance.PendingOrder.remove(user)
            return {"message":"تمت الازالة من قائمة بانتظار الدفع"}
        else:
            instance.PendingOrder.add(user)
            return {"message":"تمت الاضافة من قائمة بانتظار الدفع"}

