from rest_framework import serializers

from consumer.models import Consumer


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ('email', 'name', 'password', 'fcm_token')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Consumer.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"]
        )
        return user


class LoginSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    email = serializers.CharField()
    password = serializers.CharField()
