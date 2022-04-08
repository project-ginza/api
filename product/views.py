# Create your views here.
import operator
from functools import reduce
from typing import Optional, Any, List

from django.db import transaction, DatabaseError
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from common.views import GinzaCommonAuthAPIView
from product.models import Product, ProductDetails, ProductReview, ProductStatus
from product.serializer import serialize_product_list, serialize_product_detail_info, serialize_product_review_list, \
    serialize_product_review


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
        expressions = []
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


class ProductReviewAuthApiView(GinzaCommonAuthAPIView):

    def post(self, request, **kwargs):
        with transaction.atomic():
            # TODO : 주문 도메인 구성 후 실제 해당 유저가 주문한 상품인지 판단하는 로직 추가 필요.
            searched_product = Product.objects.get(id=kwargs['product_id'], status=ProductStatus.AVAILABLE)
            if searched_product is None:
                raise RuntimeError("리뷰 등록가능한 상품이 없습니다.")

            saved_product = ProductReview(
                product=searched_product,
                user=request.user,
                attached_image_url=request.data['review_image_url'],
                title=request.data['title'],
                details=request.data['details']
            )
            saved_product.save()
            result = Response(serialize_product_review(saved_product))
            return result

    def put(self, request, **kwargs):
        with transaction.atomic(using='default'):
            data = request.data
            user_review = ProductReview.objects.select_for_update().get(
                pk=kwargs['review_id'],
            )

            if user_review is None:
                raise RuntimeError("작성한 리뷰를 확인할 수 없습니다 [review-id : %d]" % kwargs['review_id'])

            if user_review.user.user_id != request.user.user_id:
                raise RuntimeError("리뷰 작성자만 수정 가능합니다.")

            user_review.title = data['title']
            user_review.details = data['details']
            user_review.attached_image_url = data['review_image_url']
            user_review.save()
            return Response(serialize_product_review(user_review))

    def delete(self, request, **kwargs):
        with transaction.atomic(using='default'):
            user_review = ProductReview.objects.select_for_update().get(
                pk=kwargs['review_id'],
            )

            if user_review.user.user_id != request.user.user_id:
                raise RuntimeError("리뷰 작성자만 삭제가 가능합니다.")
            result = Response(serialize_product_review(user_review))
            user_review.delete()

            return result
