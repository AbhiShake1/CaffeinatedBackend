from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        expand_products = self.context.get('expand_products', False)
        if expand_products:
            representation['product'] = ProductSerializer(instance.product).data
        return representation

    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity')
