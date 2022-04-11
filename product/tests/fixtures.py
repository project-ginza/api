from rest_framework.authtoken.admin import User

from product.models import Category, Product, ProductDetails, Currency
from product.tests.model_tests import ROOT_CATEGORY, SUB_CATEGORY, SAMPLE_PRODUCT
from user.tests import RAW_PASSWORD


def test_fixture_all_set():
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