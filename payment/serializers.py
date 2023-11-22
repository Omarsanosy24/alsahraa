from rest_framework import serializers
from .models import OrderItem
from proudects.models import *

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'



from rest_framework import serializers
from .models import order
from .serializers import OrderItemSerializer

class OrderItemSer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSer(many=True,read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = serializers.ListSerializer(child=serializers.DictField(),write_only=True)
    class Meta:
        model = order
        fields = '__all__'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order_ = super().create(validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(
                order=order_,
                product = Product.objects.get(id=order_item_data['id']).name_ar,
                quantity = order_item_data['number'],
                size = (sizes.objects.get(id = order_item_data.get('sp',None)).size_ar if order_item_data.get('sp',None) else None ),
                color = (color.objects.get(id = order_item_data.get('cp',None)).color_ar if order_item_data.get('cp',None) else None),
                price = float((sizes.objects.get(id = order_item_data.get('sp',None)).price if  order_item_data.get('sp',None) else Product.objects.get(id=order_item_data['id']).price ))

                )
        return order_