from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cart, Product
from .serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = ()
    authentication_classes = ()

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        uid = request.query_params.get('uid')
        user = cache.get(f'user_{uid}')
        if not user:
            user = get_user_model().objects.filter(id=uid).first()

            if not user:
                return Response({'error': 'User not found'})

            cache.set(f'user_{user.id}', user, None)

        product_id = request.data.get('product_id')
        product = Product.objects.select_related().get(id=product_id)

        cart_item, created = Cart.objects.get_or_create(product=product, user=user, ordered=False,
                                                        defaults={'quantity': 1})
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_items = Cart.objects.filter(user=user, ordered=False).prefetch_related()
        serializer = self.get_serializer(cart_items, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        uid = request.query_params.get('uid')
        user = cache.get(f'user_{uid}')
        if not user:
            user = get_user_model().objects.filter(id=uid).first()

            if not user:
                return Response({'error': 'User not found'})

            cache.set(f'user_{user.id}', user, None)

        cart_items = Cart.objects.filter(user=user, ordered=False).prefetch_related()
        serializer = self.get_serializer(cart_items, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def remove_from_cart(self, request):
        uid = request.query_params.get('uid')
        user = cache.get(f'user_{uid}')
        if not user:
            user = get_user_model().objects.filter(id=uid).first()

            if not user:
                return Response({'error': 'User not found'})

            cache.set(f'user_{user.id}', user, None)

        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            cart_item = Cart.objects.get(product=product, user=user, ordered=False)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()

        except ObjectDoesNotExist:
            return Response({'error': 'item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        cart_items = Cart.objects.filter(user=user, ordered=False).prefetch_related()
        serializer = self.get_serializer(cart_items, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        uid = request.query_params.get('uid')
        user = cache.get(f'user_{uid}')
        if not user:
            user = get_user_model().objects.filter(id=uid).first()

            if not user:
                return Response({'error': 'User not found'})

            cache.set(f'user_{user.id}', user, None)

        Cart.objects.filter(user=user, ordered=False).delete()

        return Response({'data': []}, status=status.HTTP_200_OK)
