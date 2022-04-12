from unittest.mock import MagicMock, Mock

from django.core.handlers.wsgi import WSGIRequest
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework import status
from django.test import TransactionTestCase
from rest_framework.test import APITestCase

from product.models import Category, Product, ProductDetails, Currency, ProductReview
from product.serializer import serialize_product_review
from product.services import ProductReviewService
from product.tests.fixtures import test_fixture_all_set
from product.tests.model_tests import ROOT_CATEGORY, SUB_CATEGORY, SAMPLE_PRODUCT, REVIEW_TITLE
from user.models import User
from user.tests import RAW_PASSWORD
from util.common import API_COMMON_PATH, GINZA_API_LOCAL_HOST

# -- https://www.django-rest-framework.org/api-guide/testing/#api-test-cases

product_review_service = ProductReviewService()
TRANSACTION_ROLLBACK_MESSAGE = '롤백 테스트 메시지'


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
            password=RAW_PASSWORD,
            user_id='test111'
        )

        ProductDetails.objects.create(
            product=test_product,
            price=1000,
            currency=Currency.KRW,
            overview="제품 전반 설명",
            scent="향 정보",
            ingredients="제품 성분 정보",
            info="주요사양정보",
        )

        review_list = ProductReview.objects.create(
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
        response_data_expect: str = "[{'review_id': 1, 'review_title': 'review-title-01', 'review_details': 'details!!!', 'review_attached_image_url': None, 'user_id': 'tester', 'review_created_at': datetime.datetime(2022, 4, 3, 13, 20, 5, 39875, tzinfo=<UTC>)}]"
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response_data_expect, response.data.__str__())


class ProductSearchViewApiTest(APITestCase):
    def setUp(self) -> None:
        print("Set Up Test Models")
        Category.objects.create(
            name=ROOT_CATEGORY
        )

        Category.objects.create(
            name=SUB_CATEGORY,
            upper_category_id=Category.objects.get(name=ROOT_CATEGORY).id
        )

        test_product1: Product = Product.objects.create(
            name=SAMPLE_PRODUCT + "1",
            short_description="short-description",
            category=Category.objects.get(name=ROOT_CATEGORY)
        )

        test_product2: Product = Product.objects.create(
            name=SAMPLE_PRODUCT + "2",
            short_description="short-description",
            category=Category.objects.get(name=SUB_CATEGORY)
        )

        test_user: User = User.objects.create(
            name='tester',
            email='test@test.com',
            password=RAW_PASSWORD,
            user_id='test111'
        )

        ProductDetails.objects.create(
            product=test_product1,
            price=1000,
            currency=Currency.KRW,
            overview="제품 전반 설명",
            scent="향 정보",
            ingredients="제품 성분 정보",
            info="주요사양정보",
        )
        pass

    """
    'SELECT 
        "product"."id", 
        "product"."name", 
        "product"."short_description", 
        "product"."category_id", 
        "product"."status" 
    FROM 
        "product" 
    WHERE 
        "product"."name" LIKE \'%product-sample1%\' ESCAPE \'\\\''
    """

    def test_product_search_name_keyword(self):
        with CaptureQueriesContext(connection) as ctx:
            url: str = GINZA_API_LOCAL_HOST + API_COMMON_PATH + 'products/search?product_name=' + SAMPLE_PRODUCT[0:3]
            print("URL : " + url)
            response: WSGIRequest = self.client.get(url)
            print("-------------------------------")
            print(*ctx.captured_queries, sep='\n')
            print("[test_product_search_name_keyword]")
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # self.assertEqual(response_data_expect, response.data.__str__())

    """
    'SELECT 
        "product"."id",
        "product"."name",
        "product"."short_description",
        "product"."category_id",
        "product"."status" 
     FROM 
        "product" 
     WHERE 
        ("product"."name" LIKE \'%produ%\' ESCAPE \'\\\' 
        AND 
        "product"."category_id" = 1)'
    """

    def test_product_search_name_keyword_and_category_id(self):
        with CaptureQueriesContext(connection) as ctx:
            url: str = GINZA_API_LOCAL_HOST + API_COMMON_PATH + 'products/search?product_name=' + SAMPLE_PRODUCT[
                                                                                                  0:5] + '&category_id=1'
            print("URL : " + url)
            response: WSGIRequest = self.client.get(url)
            print("-------------------------------")
            print(*ctx.captured_queries,
                  sep='\n')  # TODO : SELECT * FROM product_category where category_id = ?;  쿼리가 한번더 나가는 것으로 보임.
            print("[test_product_search_name_keyword_and_category_id]")
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # self.assertEqual(response_data_expect, response.data.__str__())

    """
    'SELECT 
        "product"."id", 
        "product"."name", 
        "product"."short_description", 
        "product"."category_id", 
        "product"."status" 
      FROM 
        "product" 
      WHERE 
        ("product"."name" LIKE \'%produ%\' ESCAPE \'\\\' 
        AND 
        "product"."category_id" = 1 
        AND 
        "product"."status" = 1
    """

    def test_product_search_full_conditions(self):
        with CaptureQueriesContext(connection) as ctx:
            url: str = GINZA_API_LOCAL_HOST + API_COMMON_PATH + 'products/search?product_name=' + SAMPLE_PRODUCT[
                                                                                                  0:5] + '&category_id=1&status=1'
            print("URL : " + url)
            response: WSGIRequest = self.client.get(url)
            print("-------------------------------")
            print(*ctx.captured_queries, sep='\n')
            print("[test_product_search_full_conditions]")
            print(response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # self.assertEqual(response_data_expect, response.data.__str__())


class ProductReviewAuthApiViewTest(TransactionTestCase):
    def setUp(self):
        test_fixture_all_set()

    # 리뷰 저장 롤백 테스트
    def test_product_review_create_rollback_test(self):
        with CaptureQueriesContext(connection) as ctx:
            mock_serializer = Mock(serialize_product_review, side_effect=ValueError(TRANSACTION_ROLLBACK_MESSAGE))
            with self.assertRaisesMessage(ValueError, TRANSACTION_ROLLBACK_MESSAGE):
                product_review_service.register_product_review(
                    Product.objects.get(
                        name=SAMPLE_PRODUCT + "1"
                    ).id,
                    User.objects.get(
                        name='tester',
                    ),
                    {
                        'review_image_url': '1111',
                        'title': 'title',
                        'details': 'details'
                    },
                    mock_serializer
                )

            print(*ctx.captured_queries,
                  sep='\n')
            with self.assertRaises(ProductReview.DoesNotExist):
                ProductReview.objects.get(title='title')

    # 리뷰 정상 저장 테스트
    def test_product_review_create_commit_test(self):
        with CaptureQueriesContext(connection) as ctx:
            product_review_service.register_product_review(
                Product.objects.filter(
                    name=SAMPLE_PRODUCT + "1"
                ).last().id,
                User.objects.filter(
                    name='tester',
                ).last(),
                {
                    'review_image_url': '1111',
                    'title': 'title',
                    'details': 'details'
                },
                serialize_product_review
            )

        print(*ctx.captured_queries, sep='\n')
        searched_review = ProductReview.objects.filter(title='title')
        self.assertIsNotNone(searched_review)

    # 리뷰 정상 수정 테스트
    def test_product_review_update_commit_test(self):
        with CaptureQueriesContext(connection) as ctx:
            saved_review = ProductReview.objects.create(
                product=Product.objects.filter(
                    name=SAMPLE_PRODUCT + "1"
                ).last(),
                user=User.objects.filter(
                    name='tester',
                ).last(),
                attached_image_url='1111',
                title='title',
                details='details'
            )

            self.assertEquals('1111', saved_review.attached_image_url)
            self.assertEquals('title', saved_review.title)
            self.assertEquals('details', saved_review.details)

            product_review_service.modify_product_review(saved_review.id, User.objects.filter(
                name='tester',
            ).last(), {
                                                             'review_image_url': 'url123',
                                                             'title': 'eltit',
                                                             'details': 'sliated'
                                                         })
            updated_review = ProductReview.objects.get(id=saved_review.id)
            self.assertEquals(saved_review.id, updated_review.id)
            self.assertEquals('url123', updated_review.attached_image_url)
            self.assertEquals('eltit', updated_review.title)
            self.assertEquals('sliated', updated_review.details)
