from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    items = serializers.ListField()

    class Meta:
        model = Order
        fields = ('id', 'student', 'items', 'date_ordered', 'total_price', 'status')

    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        order.save()
        return order

    def get_id(self, obj):
        return obj.pk
