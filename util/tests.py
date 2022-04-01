# =============================
# Serializer Test
import json

from django.test import SimpleTestCase

from product.models import Product, Category, ProductStatus
from product.tests import ROOT_CATEGORY, SAMPLE_PRODUCT
from util.serializer import serialize_product, serialize_product_list, ginza_general_json_serializer, \
    INVALID_TYPE_EXCEPTION_MESSAGE


class CustomSerializerTestCase(SimpleTestCase):
    databases = '__all__'

    # TC 1 : Product 단건 Dictionary Data로 직렬화 로직 테스트
    def test_serialize_product_value(self):
        sample_product = Product.objects.create(
            name=SAMPLE_PRODUCT,
            short_description="short-description",
            category=Category.objects.create(
                name=ROOT_CATEGORY
            )
        )

        result = serialize_product(
            sample_product
        )

        print(result)
        self.assertEqual(result['id'], sample_product.id)
        self.assertEqual(result['name'], sample_product.name)
        self.assertEqual(result['short_description'], sample_product.short_description)
        self.assertEqual(result['category'], sample_product.category.name)
        self.assertEqual(ProductStatus.AVAILABLE, sample_product.status)

    # TC 2 : Product 단건 결과가 없을 시 빈 Dict 리턴 확인
    def test_serialize_product_empty(self):
        result = serialize_product(
            None
        )
        print(result)
        self.assertFalse(bool(result))  # Empty Dict

    # TC 3 : Product 다건 Dictionary Data로 직렬화 로직 테스트
    def test_serialize_product_list(self):
        sample_product_list = [
            Product.objects.create(
                name=SAMPLE_PRODUCT + "1",
                short_description="short-description",
                category=Category.objects.create(
                    name=ROOT_CATEGORY
                )
            ),
            Product.objects.create(
                name=SAMPLE_PRODUCT + "2",
                short_description="short-description",
                category=Category.objects.create(
                    name=ROOT_CATEGORY
                )
            ),
            Product.objects.create(
                name=SAMPLE_PRODUCT + "3",
                short_description="short-description",
                category=Category.objects.create(
                    name=ROOT_CATEGORY
                )
            )
        ]

        result = serialize_product_list(
            sample_product_list
        )

        print(result)
        self.assertEqual(3, len(result))
        self.assertEqual(SAMPLE_PRODUCT + "1", result[0].get('name'))

    # TC 4 : Product 다건 Dictionary Data로 직렬화 로직 테스트(empty)
    def test_serialize_product_list_empty(self):
        sample_empty_list = []

        result = serialize_product_list(
            sample_empty_list
        )

        print(result)
        self.assertEqual(0, len(result))

    # TC 5 : 커스텀 General JSON serializer 함수 테스트(Type Error : Not iterable)
    def test_ginza_general_json_serializer_not_iterable(self):
        # DRF에서는 Iterable Object가 아니면 serialize가 안되나봄...
        with self.assertRaisesMessage(TypeError, "'Category' object is not iterable"):
            ginza_general_json_serializer(
                Category.objects.create(
                    name=ROOT_CATEGORY
                )
            )

    # TC 6 : 커스텀 General JSON serializer 함수 테스트(예외 처리)
    def test_ginza_general_json_serializer_not_allowd_type_error(self):
        # SERIALIZE_TYPE_ALLOW_LIST 에 없는 타입으로 직렬화 시도시 ValueError 리턴
        with self.assertRaisesMessage(ValueError, INVALID_TYPE_EXCEPTION_MESSAGE):
            ginza_general_json_serializer(
                SampleClass
            )

    # TC 7 : 커스텀 General JSON serializer 함수 테스트
    def test_ginza_general_json_serializer(self):
        Category.objects.create(
            name=ROOT_CATEGORY
        )

        result = ginza_general_json_serializer(
            Category.objects.all()
        )

        print('-----------JSON Parsing Result --------------------------')
        print(result)
        print('-----------JSON Parsing Result --------------------------')
        self.assertIsNotNone(result)
        json_object = json.loads(result)
        self.assertIsNotNone(json_object[0]['fields']) # JSON

# =============================

class SampleClass:
    def __init__(self):
        print("hello")
