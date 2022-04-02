from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# -- https://www.django-rest-framework.org/api-guide/testing/#api-test-cases

from product.models import Category, Product
from product.tests.model_tests import ROOT_CATEGORY, SUB_CATEGORY, SAMPLE_PRODUCT
from util.common import API_COMMON_PATH


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

        Product.objects.create(
            name=SAMPLE_PRODUCT,
            short_description="short-description",
            category=Category.objects.get(name=ROOT_CATEGORY)
        )

    def test_product_list_retrieve(self):
        url = 'http://localhost:8000/'+API_COMMON_PATH+'products/'
        response = self.client.get(url)
        print("-------------------------------")
        print("[test_product_list_retrieve]")
        print(response.data)
        response_data_expect = "[{'id': 1, 'name': 'product-sample', 'short_description': 'short-description', 'category': 'root-category', 'status': '0'}]"
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 200 OK만 가정
        self.assertEqual(response_data_expect, response.data.__str__())
