# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.serializer import serialize_product_list


class ProductList(APIView):
    def get(self, request):
        # product_list = [serialize_product(product) for product in Product.objects.all()]
        serialized_product_list = serialize_product_list(Product.objects.all())
        return Response(serialized_product_list)
