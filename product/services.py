import operator
from functools import reduce
from typing import Dict, Any, List, Optional, Callable

from django.db.models import Q
from rest_framework.response import Response

from product.models import Product, ProductDetails, ProductReview, ProductStatus
from product.serializer import serialize_product_list, serialize_product_detail_info, serialize_product_review_list, \
    serialize_product_review
from user.models import User
from util.aspects import ginza_transactional


class ProductService:
    def retrieve_product_list(self) -> List[Dict[str, Any]]:
        return serialize_product_list(Product.objects.all())

    def search_product_list(self, searchParam: Dict[str, Any]):
        queryset = Product.objects.all()
        expressions = []
        if searchParam.get('product_name', False):
            expressions.append(Q(name__contains=searchParam['product_name']))
        if searchParam.get('category_id', False):
            expressions.append(Q(category_id=searchParam['category_id']))
        if searchParam.get('status', False):
            expressions.append(Q(status=searchParam['status']))

        filtered_product_list = queryset.filter(reduce(operator.and_, expressions))
        return serialize_product_list(
            filtered_product_list
        )


class ProductDetailsService:
    def retrieve_product_detail(self, product_id) -> Optional[Dict[str, Any]]:
        return serialize_product_detail_info(ProductDetails \
                                             .objects \
                                             .select_related('product') \
                                             .select_related('product__category') \
                                             .get(product_id=product_id))


class ProductReviewService:
    def retrieve_product_review_list(self, product_id) -> List[Dict[str, Any]]:
        return serialize_product_review_list(ProductReview \
                                             .objects \
                                             .filter(product__id=product_id) \
                                             .select_related('user') \
                                             .order_by('created_at'))

    @ginza_transactional
    def register_product_review(self, product_id: int, user: User, input: Dict[str, Any], serializer: Callable[
        [ProductReview], Dict[str, Any]]) -> Response:
        # TODO : 주문 도메인 구성 후 실제 해당 유저가 주문한 상품인지 판단하는 로직 추가 필요.
        try:
            searched_product = Product.objects.get(id=product_id, status=ProductStatus.AVAILABLE)
        except Product.DoesNotExist:
            raise RuntimeError("리뷰 등록가능한 상품이 없습니다.")

        saved_product = ProductReview.objects.create(
            product=searched_product,
            user=user,
            attached_image_url=input.get('review_image_url', None),
            title=input.get('title'),
            details=input.get('details')
        )
        # raise Exception("테스트") # 여기서 Exception이 Throw 되면 ProductReview Rollback 진행
        return Response(serializer(saved_product))

    @ginza_transactional
    def modify_product_review(self, review_id: int, user: User, input: Dict[str, Any]) -> Response:
        user_review = ProductReview.objects.select_for_update(of=('self',)).get(
            pk=review_id,
            user_id=user.id
        )

        if user_review is None:
            raise RuntimeError("작성한 리뷰를 확인할 수 없습니다 [review-id : %d]" % review_id)

        user_review.title = input.get('title', None)
        user_review.details = input.get('details', None)
        user_review.attached_image_url = input.get('review_image_url', None)
        user_review.save()
        return Response(serialize_product_review(user_review))

    @ginza_transactional
    def delete_product_review(self, review_id: int, user: User) -> Response:
        user_review = ProductReview.objects.select_for_update().get(
            pk=review_id,
            user_id=user.id
        )

        result = Response(serialize_product_review(user_review))
        user_review.delete()

        return result
