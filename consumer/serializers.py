from rest_framework import serializers

from .models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Consumer
        fields = ('id', 'name', 'email', 'fcm_token')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.fcm_token = validated_data.get('fcm_token', instance.fcm_token)
        instance.save()
        return instance

    def get_id(self, obj):
        return obj.pk
