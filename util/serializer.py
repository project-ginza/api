import logging
from typing import Dict, Any, List

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.http import HttpResponse
from rest_framework import serializers

from product.models import Product

SERIALIZE_TYPE_ALLOW_LIST = [models.query.QuerySet, models.Model,]

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
        return {}

    return {
        'id': product.id,
        'name': product.name,
        'short_description': product.short_description,
        'category': product.category.name,
        'status': product.status.__str__()
    }


# Function Base Product Model Serializer(List)
def serialize_product_list(product_list: List[Product]) -> List[Dict[str, Any]]:
    return list(map(serialize_product, product_list))


# General Functional Serializer
def ginza_general_json_serializer(model: object):
    print(type(model))
    for allowed_type in SERIALIZE_TYPE_ALLOW_LIST:
        if issubclass(type(model), allowed_type):
            return serialize('json', model, cls=DjangoJSONEncoder)
    # TODO : Detailed exception checking implementation required
    raise ValueError(INVALID_TYPE_EXCEPTION_MESSAGE)


class GinzaGeneralHttpResponse(HttpResponse):
    def __init__(self, content, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content_type = 'application/json'
        self.content = content
