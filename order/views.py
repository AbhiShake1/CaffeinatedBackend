from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart
from product.models import Product
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = ()
    authentication_classes = ()

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        queryset = self.queryset.filter(user=uid)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    def create(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        user = cache.get(f'user_{uid}')
        if not user:
            user = get_user_model().objects.filter(id=uid).first()

            if not user:
                return Response({'error': 'User not found'})

            cache.set(f'user_{user.id}', user, None)
        carts = Cart.objects.filter(user=user)
        if not carts:
            return Response({'error': 'Cart not found'})

        order = Order.objects.create(user=user)
        order.carts.set(carts)
        order.save()

        carts.update(ordered=True)
        queryset = Order.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})

    @action(detail=False, methods=['post'])
    def create_instant_order(self, request, *args, **kwargs):
        carts = request.data.get('carts')
        uid = request.query_params.get('uid')
        user = cache.get(f'user_{uid}')
        if not user:
            user = get_user_model().objects.filter(id=uid).first()

            if not user:
                return Response({'error': 'User not found'})

            cache.set(f'user_{user.id}', user, None)

        cart_instances = []
        for cart in carts:
            product = Product.objects.get(id=cart['product']['id'])
            cart_instances.append(Cart.objects.create(user=user, product=product, quantity=cart['quantity']))

        order = Order.objects.create(user=user)
        order.carts.set(cart_instances)
        order.save()

        for cart in cart_instances:
            cart.ordered = True
            cart.save()

        queryset = Order.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})
