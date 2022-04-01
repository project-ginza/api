from django.http import JsonResponse
# Create your views here.
from rest_framework.decorators import api_view

from product.models import Product
from util.serializer import serialize_product_list


# TODO : api_view Test Required

@api_view(['GET'])  # 일단 GET 만 정의
def product_list(request):
    if request.method == 'GET':
        product_list = Product.objects.all()
        # serializer = ProductSerializer(product_list, many=True)
        serializer = serialize_product_list(product_list)
        return JsonResponse(serializer, safe=False)
