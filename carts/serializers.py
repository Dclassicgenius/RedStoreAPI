
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from store.serializers import ProductSerializer
from .models import Cart, CartItem 


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['cart_id', 'date_added',]

    
    def create(self, validated_data):
        
        validated_data['cart_id'] = self.context.get('request').session.session_key
        cart = Cart.objects.create(**validated_data)
        return cart


class CartItemSerializer(FlexFieldsModelSerializer):
    sub_total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'cart', 'sub_total','quantity', 'user',]
        read_only_fields = ['id', 'user', 'is_active', 'sub_total',]

        expandable_fields = {
            'product': (ProductSerializer, {'many': True}),
            'cart': (CartSerializer, {'many':False})
        }
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def get_sub_total(self, obj):
        return obj.sub_total

  