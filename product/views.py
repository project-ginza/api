# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from common.views import GinzaCommonAuthAPIView
from product.serializer import serialize_product_review, PostProductReviewAuthApiViewRequestBodySerializer, \
    PutProductReviewAuthApiViewRequestBodySerializer
from product.services import ProductService, ProductDetailsService, ProductReviewService

product_service = ProductService()
product_details_service = ProductDetailsService()
product_review_service = ProductReviewService()


class ProductList(APIView):

    def get(self, request):
        return Response(product_service.retrieve_product_list())


class ProductDetailsView(APIView):

    def get(self, request, **kwargs):
        return Response(product_details_service.retrieve_product_detail(kwargs['product_id']))


class ProductReviewListView(APIView):

    def get(self, request, **kwargs):
        return Response(product_review_service.retrieve_product_review_list(kwargs['product_id']))


class ProductSearchListView(APIView):

    def get(self, request, **kwargs):
        return Response(product_service.search_product_list(request.query_params))


class ProductReviewAuthApiView(GinzaCommonAuthAPIView):

    @swagger_auto_schema(request_body=PutProductReviewAuthApiViewRequestBodySerializer)
    def put(self, request, **kwargs):
        return product_review_service.modify_product_review(kwargs['review_id'],
                                                            request.user,
                                                            request.data)

    @swagger_auto_schema()
    def delete(self, request, **kwargs):
        return product_review_service.delete_product_review(kwargs['review_id'], request.user)


class ProductReviewAuthApiRegisterView(GinzaCommonAuthAPIView):
    @swagger_auto_schema(request_body=PostProductReviewAuthApiViewRequestBodySerializer)
    def post(self, request, **kwargs):
        return product_review_service.register_product_review(kwargs['product_id'],
                                                              request.user,
                                                              request.data,
                                                              serialize_product_review)
