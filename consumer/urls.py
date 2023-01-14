from django.urls import path
from .views import *

urlpatterns = [
    path('', ConsumerView.as_view(), name='current-user'),
]
