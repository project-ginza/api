import logging
from typing import Dict, Any, List

from django.db import models
from rest_framework import serializers

from product.models import Product

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
def serialize_product(product: Product) -> Dict[str, Any]:
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