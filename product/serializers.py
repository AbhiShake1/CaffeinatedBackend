from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'description', 'available', 'rating', 'image_url')

    def get_id(self, obj):
        return obj.pk

    # def get_image_url(self, obj):
    #     request = self.context.get("request")
    #     if obj.image:
    #         return request.build_absolute_uri(obj.image.url)
    #     else:
    #         filename = "default.png"
    #         return request.build_absolute_uri(reverse('products:default_image', kwargs={'filename': filename}))
