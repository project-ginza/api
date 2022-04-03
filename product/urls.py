from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from product import views
from util.common import API_COMMON_PATH

urlpatterns = [
    path(API_COMMON_PATH + 'products/', views.ProductList.as_view()),
    path(API_COMMON_PATH + 'product/<int:product_id>', views.ProductDetailsView.as_view()),
    path(API_COMMON_PATH + 'product/<int:product_id>/reviews', views.ProductReviewListView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
