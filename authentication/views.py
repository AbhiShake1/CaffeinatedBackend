from django.contrib.auth import logout, login
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from consumer.models import Consumer
from .serializers import ConsumerSerializer, LoginSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = ConsumerSerializer
    permission_classes = (AllowAny,)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        try:
            user = Consumer.objects.get(email=email)
        except:
            return Response({"error": "User with that email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        return Response(ConsumerSerializer(user, context=self.get_serializer_context()).data)


class LogoutView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
