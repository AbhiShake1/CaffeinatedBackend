from django.urls import path, include
from rest_framework import routers

from .views import OrderViewSet

router = routers.DefaultRouter()
router.register('', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
