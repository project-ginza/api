from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from product.views import ProductList, ProductSearchListView, ProductDetailsView, ProductReviewListView, \
    ProductReviewAuthApiView
from util.common import API_COMMON_PATH

urlpatterns = [
    path(API_COMMON_PATH + 'products', ProductList.as_view()),
    path(API_COMMON_PATH + 'product/<int:product_id>', ProductDetailsView.as_view()),
    path(API_COMMON_PATH + 'product/<int:product_id>/reviews', ProductReviewListView.as_view()),
    path(API_COMMON_PATH + 'products/search', ProductSearchListView.as_view()),
    path(API_COMMON_PATH + 'product/<int:product_id>/review/<int:review_id>', ProductReviewAuthApiView.as_view()),
    path(API_COMMON_PATH + 'product/<int:product_id>/review', ProductReviewAuthApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
