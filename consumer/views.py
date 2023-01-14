from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .serializers import ConsumerSerializer


class ConsumerView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = ConsumerSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            serializer = ConsumerSerializer(request.user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)
