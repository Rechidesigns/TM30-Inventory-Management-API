from rest_framework import serializers
from .models import Product, Cart


class ProductSerializer(serializers.ModelSerializer):
    orders = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'quantity', 'orders']

class CartSerializer(serializers.ModelSerializer):
    cart_content = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user' ,'product_item', 'product_quantity', 'product_cost', 'date_of_ordering', 'status', 'cart_products']
        
class CartReqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['cart_products', 'product_quantity']

class ProductUserSerializer(serializers.ModelSerializer):
    orders_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'quantity', 'orders_count']