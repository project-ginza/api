import datetime

from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Category, Product, ProductDetails, Currency, ProductReview
from product.tests.model_tests import ROOT_CATEGORY, SUB_CATEGORY, SAMPLE_PRODUCT, REVIEW_TITLE
from user.models import User
from user.tests import RAW_PASSWORD
from util.common import API_COMMON_PATH, GINZA_API_LOCAL_HOST


# -- https://www.django-rest-framework.org/api-guide/testing/#api-test-cases


class ProductApiTests(APITestCase):
    def setUp(self) -> None:
        print("Set Up Test Models")
        Category.objects.create(
            name=ROOT_CATEGORY
        )

        Category.objects.create(
            name=SUB_CATEGORY,
            upper_category_id=Category.objects.get(name=ROOT_CATEGORY).id
        )

        test_product: Product = Product.objects.create(
            name=SAMPLE_PRODUCT,
            short_description="short-description",
            category=Category.objects.get(name=ROOT_CATEGORY)
        )

        test_user: User = User.objects.create(
            name='tester',
            email='test@test.com',
            password=RAW_PASSWORD
        )

        ProductDetails.objects.create(
            product=test_product,
            price=1000,
            currency=Currency.KRW,
            overview="제품 전반 설명",
            scent="향 정보",
            ingredients="제품 성분 정보",
            info="주요사양정보",
            modified_at=datetime.datetime.now()
        )

        review_list = ProductReview.objects.create(
            modified_at=datetime.datetime.now(),
            product=test_product,
            title=REVIEW_TITLE + '-01',
            details='details!!!',
            attached_image_url=None,
            user=test_user
        )
        pass

    def test_product_list_retrieve(self):
        url = GINZA_API_LOCAL_HOST + API_COMMON_PATH + 'products/'
        response = self.client.get(url)
        print("-------------------------------")
        print("[test_product_list_retrieve]")
        print(response.data)
        response_data_expect: str = "[{'id': 1, 'name': 'product-sample', 'short_description': 'short-description', 'category': 'root-category', 'status': '0'}]"
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK만 가정
        self.assertEqual(response_data_expect, response.data.__str__())

    # TC 2 : 제품 상세정보 단건조회 테스트
    # /api/v1/product/<int:product_id>
    def test_product_details_retrieve(self):
        saved_product: Product = Product.objects.get(name=SAMPLE_PRODUCT)
        url: str = GINZA_API_LOCAL_HOST + API_COMMON_PATH + 'product/' + saved_product.id.__str__()
        response: WSGIRequest = self.client.get(url)
        print("-------------------------------")
        print("[test_product_details_retrieve]")
        print(response.data)
        response_data_expect = "{'product_id': 1, 'product_overview': '제품 전반 설명', 'category_name': 'root-category', 'product_name': 'product-sample', 'product_description': '주요사양정보', 'product_ingredients': '제품 성분 정보', 'product_price': Decimal('1000.00')}"
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response_data_expect, response.data.__str__())

    def test_product_review_list_by_product_id(self):
        saved_product: Product = Product.objects.get(name=SAMPLE_PRODUCT)
        url: str = GINZA_API_LOCAL_HOST + API_COMMON_PATH + 'product/' + saved_product.id.__str__() + '/reviews'
        response: WSGIRequest = self.client.get(url)
        print("-------------------------------")
        print("[test_product_review_list_by_product_id]")
        print(response.data)
        response_data_expect : str = "[{'review_id': 1, 'review_title': 'review-title-01', 'review_details': 'details!!!', 'review_attached_image_url': None, 'user_id': 'tester', 'review_created_at': datetime.datetime(2022, 4, 3, 13, 20, 5, 39875, tzinfo=<UTC>)}]"
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response_data_expect, response.data.__str__())
