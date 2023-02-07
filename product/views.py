from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        return {"request": self.request}

    @action(detail=True, methods=['get'])
    def for_uid(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        if not uid:
            return Response({'error': 'uid is required'})

        product = self.get_object()
        serializer = self.get_serializer(product)
        user = get_user_model().objects.filter(id=uid).first()

        if not user:
            return Response({'error': 'uid not found'})

        data = serializer.data

        data['bookmarked'] = product in user.bookmarked_products.all()
        return Response({'data': data})

    @action(detail=False, methods=['get'])
    def all(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        if not uid:
            return Response({'error': 'uid is required'})

        product = self.get_queryset()
        serializer = self.get_serializer(product, many=True)
        user = get_user_model().objects.filter(id=uid).first()

        if not user:
            return Response({'error': 'uid not found'})

        data = serializer.data

        for i in range(0, len(data)):
            data[i]['bookmarked'] = product[i] in user.bookmarked_products.all()

        return Response({'data': data})

    @action(detail=False, methods=['get'])
    def all_bookmarked(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        if not uid:
            return Response({'error': 'uid is required'})

        product = self.get_queryset().filter(bookmarked_by=uid)
        serializer = self.get_serializer(product, many=True)

        data = serializer.data

        for i in range(0, len(data)):
            data[i]['bookmarked'] = True

        return Response({'data': data})

    @action(detail=True, methods=['get'])
    def bookmark(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        if not uid:
            return Response({'error': 'uid is required'})

        product = self.get_object()
        user = get_user_model().objects.filter(id=uid).first()

        if not user:
            return Response({'error': 'uid not found'})
        user.bookmarked_products.add(product)
        user.save()
        return Response({'message': 'Product bookmarked'})

    @action(detail=True, methods=['get'])
    def remove_bookmark(self, request, *args, **kwargs):
        uid = request.query_params.get('uid')
        if not uid:
            return Response({'error': 'uid is required'})

        product = self.get_object()
        user = get_user_model().objects.filter(id=uid).first()

        if not user:
            return Response({'error': 'uid not found'})
        user.bookmarked_products.remove(product)
        user.save()
        return Response({'message': 'Product bookmark removed'})
