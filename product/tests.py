from django.db import connection
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext

# Product Model Transaction Test
from product.models import Category, Product, ProductStatus

# Create your tests here.

ROOT_CATEGORY = 'root-category'
SUB_CATEGORY = 'sub-category'

SAMPLE_PRODUCT = 'product-sample'


class CategoryTestCase(TransactionTestCase):
    def setUp(self):
        print("Set Up Test Models")
        Category.objects.create(
            name=ROOT_CATEGORY
        ).save()

        Category.objects.create(
            name=SUB_CATEGORY,
            upper_category_id=Category.objects.get(name=ROOT_CATEGORY).id
        ).save()

    # TC 1 : Root-Category와 Sub-Category가 의도에 맞게 저장되는지 확인
    # Root -> upper_category_id = NULL / sub -> root.id
    def test_category_info(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_category_info================")

            searched_root = Category.objects.get(name=ROOT_CATEGORY)
            searched_sub = Category.objects.get(name=SUB_CATEGORY)
            self.assertIsNone(searched_root.upper_category_id)
            self.assertEqual(searched_root.id, searched_sub.upper_category_id)

            print(*ctx.captured_queries, sep='\n')
            print("============================================")


class ProductTestCase(TransactionTestCase):
    def setUp(self):
        print("Set Up Test Models")
        saved_root_category = Category.objects.create(
            name=ROOT_CATEGORY
        ).save()

        Category.objects.create(
            name=SUB_CATEGORY,
            upper_category_id=Category.objects.get(name=ROOT_CATEGORY).id
        ).save()

        Product.objects.create(
            name=SAMPLE_PRODUCT,
            short_description="short-description",
            category=Category.objects.get(name=ROOT_CATEGORY)
        )

    # TC 1 : 기본 상품 상태(ProductStatus.AVAILABLE) 정상 등록 여부 확인
    def test_product_default_status(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_product_default_status================")
            searched_product = Product.objects.get(name=SAMPLE_PRODUCT)
            self.assertEqual(ProductStatus.AVAILABLE, searched_product.status)
            print("============================================")