from rest_framework import serializers

from cart.serializers import CartSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    carts = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ['date_ordered', 'status', 'carts']
