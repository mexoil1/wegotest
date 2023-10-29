from rest_framework import serializers

from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер продуктов"""
    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'content', 'price')


class GetOrderSerializer(serializers.ModelSerializer):
    """Сериалайзер продукта"""
    class Meta:
        model = Order
        fields = '__all__'
