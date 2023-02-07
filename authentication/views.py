import socket

import psutil
from django.contrib.auth import logout, login, get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from CaffeinatedBackend.settings import SENDER_EMAIL
from consumer.serializers import ConsumerSerializer
from .serializers import LoginSerializer, SignupSerializer


class ChangePasswordView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        user = cache.get(f'user_{user_id}')
        if not user:
            try:
                user = get_user_model().objects.get(pk=user_id)
                cache.set(f'user_{user_id}', user, None)
            except get_user_model().DoesNotExist:
                return Response({'error': 'User not found'})

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if user.check_password(old_password):
            get_user_model().objects.filter(pk=user_id).update(password=make_password(new_password))
            return Response({'message': 'password successfully changed'})
        else:
            return Response({'error': 'incorrect old password'})


class SignupView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'data': ConsumerSerializer(user).data}, status=HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            cache.set(f'user_{user.id}', user, None)

        if user is not None and user.check_password(password):
            login(request, user)
            user_data = ConsumerSerializer(user).data
            user_data.pop('password', None)
            return Response({'data': user_data}, status=HTTP_200_OK)
        else:
            return Response({"error": "Invalid email or password."})


class LogoutView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendPasswordResetLinkView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(email=email)
        except:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build password reset link
        host = request.get_host()

        if host.startswith('127.0.0.1') or host.startswith('localhost'):
            ip_lhost = next(
                (addr.address for net_if,
                addrs in psutil.net_if_addrs().items()
                 for addr in addrs if addr.family == socket.AF_INET
                 and addr.address.startswith('192')
                 ),
                None
            )
            host = f'{ip_lhost}:{request.get_port()}'
        reset_link = f"http://{host}/auth/reset-password/{uid}/{token}/"

        # Send password reset link to email
        send_mail(
            'Password Reset',
            f'Please click the link to reset your password: {reset_link}',
            SENDER_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response({'message': 'Password reset link sent to email'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            return render(request, 'reset_password.html', {'user_name': user.name})
        else:
            return JsonResponse({'error': 'Reset link expired'},
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/html')

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            if not (password and confirm_password):
                return JsonResponse({'error': 'Password and Confirm Password are required'},
                                    status=status.HTTP_400_BAD_REQUEST, content_type='text/html')
            if password != confirm_password:
                return JsonResponse({'error': 'Password and Confirm Password do not match'},
                                    status=status.HTTP_400_BAD_REQUEST, content_type='text/html')
            user.set_password(password)
            user.save()
            return JsonResponse({'message': 'Password reset successfully'}, status=status.HTTP_200_OK,
                                content_type='text/html')
        else:
            return JsonResponse({'error': 'Reset link expired'}, status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/html', )
