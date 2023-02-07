from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        if self.request.method == 'GET':
            uid = self.request.query_params.get('uid', None)
            if uid is None:
                raise ValidationError({'error': 'User ID (uid) query parameter is required'})

            user = cache.get(f'user_{uid}')
            if not user:
                user = get_user_model().objects.filter(id=uid).first()

                if not user:
                    return Response({'error': 'User not found'})

                cache.set(f'user_{user.id}', user, None)
            return Notification.objects.filter(user=user).order_by('-created_at')
        else:
            return Notification.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    def destroy(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.delete()
        return Response(status=204)
