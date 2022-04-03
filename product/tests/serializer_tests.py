# =============================
# Serializer Test
import datetime
from typing import Optional, Any

from django.test import SimpleTestCase

from product.models import Product, Category, ProductStatus, ProductDetails, Currency
from product.serializer import serialize_product, serialize_product_list, \
    INVALID_TYPE_EXCEPTION_MESSAGE, serialize_product_detail_info
from product.tests.model_tests import SAMPLE_PRODUCT, ROOT_CATEGORY


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

    def test_serialize_product_detail_info(self):
        Category.objects.create(
            name=ROOT_CATEGORY,
        )

        product: Product = Product.objects.create(
            name=SAMPLE_PRODUCT,
            short_description="short-description",
            category=Category.objects.get(name=ROOT_CATEGORY)
        )

        test_details = ProductDetails.objects.create(
            product=product,
            price=1000,
            currency=Currency.KRW,
            overview="제품 전반 설명",
            scent="향 정보",
            ingredients="제품 성분 정보",
            info="주요사양정보",
            modified_at=datetime.datetime.now()
        )

        result: Optional[dict[str, Any]] = serialize_product_detail_info(test_details)
        print(result.__str__())
        self.assertEqual(product.id, result['product_id'])
        self.assertEqual(test_details.overview, result['product_overview'])
        self.assertEqual(product.category.name, result['category_name'])
        self.assertEqual(product.name, result['product_name'])
        self.assertEqual(test_details.info, result['product_description'])
        self.assertEqual(test_details.price, result['product_price'])
        self.assertEqual(Currency.KRW.label, result['currency'])


# =============================

class SampleClass:
    def __init__(self):
        print("hello")
