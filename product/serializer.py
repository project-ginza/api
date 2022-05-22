from __future__ import annotations

import logging
from typing import Dict, Any, List

from django.db import models
from rest_framework import serializers

from product.models import Product, ProductDetails, ProductReview, Currency

SERIALIZE_TYPE_ALLOW_LIST = [models.query.QuerySet, models.Model, ]

INVALID_TYPE_EXCEPTION_MESSAGE = '[serializer-error] not allowed JSON Serialize Type'

logger = logging.getLogger('api')


# Class Base Model-Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'short_description', 'category', 'status']
        read_only_fields = fields


# Function Base Product Model Serializer
def serialize_product(product: Product) -> Dict[str, Any] | None:
    if product is None:
        return None

    return {
        'id': product.id,
        'name': product.name,
        'short_description': product.short_description,
        'category': product.category.name,
        'status': product.status.__str__(),
    }


# Function Base Product Model Serializer(List)
def serialize_product_list(product_list: List[Product]) -> List[Dict[str, Any]]:
    return list(map(serialize_product, product_list))


def serialize_product_detail_info(product_details: ProductDetails) -> Dict[str, Any] | None:
    if product_details is None:
        return None
    return {
        'product_id': product_details.product.id,
        'product_overview': product_details.overview,
        'category_name': product_details.product.category.name,
        'product_name': product_details.product.name,
        'product_description': product_details.info,
        'product_ingredients': product_details.ingredients,
        'product_price': product_details.price,
        'currency': Currency.labels[product_details.currency]
    }


def serialize_product_review(product_review: ProductReview) -> Dict[str, Any] | None:
    if product_review is None:
        return None
    return {
        'review_id': product_review.id,
        'review_title': product_review.title,
        'review_details': product_review.details,
        'review_attached_image_url': product_review.attached_image_url,
        'user_id': product_review.user.name,
        'review_created_at': product_review.created_at
    }


def serialize_product_review_list(product_review_list: List[ProductReview]) -> List[Dict[str, Any]]:
    return list(map(serialize_product_review, product_review_list))


# ----------------------------
# ---For Swagger
# ----------------------------

class PostProductReviewAuthApiViewRequestBodySerializer(serializers.Serializer):
    review_image_url = serializers.CharField(help_text='Image Url')
    title = serializers.CharField(help_text='Title')
    details = serializers.CharField(help_text='상세')

class PutProductReviewAuthApiViewRequestBodySerializer(serializers.Serializer):
    review_image_url = serializers.CharField(help_text='Image Url')
    title = serializers.CharField(help_text='Title')
    details = serializers.CharField(help_text='상세')
