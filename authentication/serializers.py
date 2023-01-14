from django.contrib.auth import get_user_model
from rest_framework import serializers


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'password', 'fcm_token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
