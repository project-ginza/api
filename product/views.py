# Create your views here.
import operator
from functools import reduce
from typing import Optional, Any, List

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, ProductDetails, ProductReview
from product.serializer import serialize_product_list, serialize_product_detail_info, serialize_product_review_list


class ProductList(APIView):
    def get(self, request):
        # product_list = [serialize_product(product) for product in Product.objects.all()]
        serialized_product_list: List[dict[str, Any]] = serialize_product_list(Product.objects.all())
        return Response(serialized_product_list)


class ProductDetailsView(APIView):
    def get(self, request, **kwargs):
        response: Optional[dict[str, Any]] = serialize_product_detail_info(ProductDetails \
                                                                           .objects \
                                                                           .select_related('product') \
                                                                           .select_related('product__category') \
                                                                           .get(product_id=kwargs['product_id']))
        return Response(response)


class ProductReviewListView(APIView):
    def get(self, request, **kwargs):
        response: List[dict[str, Any]] = serialize_product_review_list(ProductReview \
                                                                       .objects \
                                                                       .filter(product__id=kwargs['product_id']) \
                                                                       .select_related('user') \
                                                                       .order_by('created_at'))
        return Response(response)


class ProductSearchListView(APIView):
    def get(self, request, **kwargs):
        queryset = Product.objects.all()
        expressions =[]
        if request.query_params.get('product_name', False):
            expressions.append(Q(name__contains=request.query_params['product_name']))
        if request.query_params.get('category_id', False):
            expressions.append(Q(category_id=request.query_params['category_id']))
        if request.query_params.get('status', False):
            expressions.append(Q(status=request.query_params['status']))

        filtered_product_list = queryset.filter(reduce(operator.and_, expressions))
        response: List[dict[str, Any]] = serialize_product_list(
            filtered_product_list
        )
        return Response(response)
