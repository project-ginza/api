from django.db import connection
from django.test import TransactionTestCase
from django.test.utils import CaptureQueriesContext

from product.models import Category, Product, ProductStatus, ProductDetails, Currency, ProductReview
from product.serializer import serialize_product_review_list
from user.models import User
from user.tests import RAW_PASSWORD

ROOT_CATEGORY = 'root-category'
SUB_CATEGORY = 'sub-category'

SAMPLE_PRODUCT = 'product-sample'
REVIEW_TITLE = 'review-title'

class CategoryTestCase(TransactionTestCase):
    def setUp(self):
        with CaptureQueriesContext(connection) as ctx:
            print("Set Up Test Models")
            Category.objects.create(
                name=ROOT_CATEGORY
            )

            Category.objects.create(
                name=SUB_CATEGORY,
                upper_category_id=Category.objects.get(name=ROOT_CATEGORY).id
            )
            print(*ctx.captured_queries, sep='\n')
            pass

    # TC 1 : Root-Category와 Sub-Category가 의도에 맞게 저장되는지 확인
    # Root -> upper_category_id = NULL / sub -> root.id
    def test_category_info(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_category_info================")

            searched_root = Category.objects.get(name=ROOT_CATEGORY)
            searched_sub = Category.objects.get(name=SUB_CATEGORY)
            # self.assertIsNone(searched_root.upper_category_id)
            self.assertEqual(searched_root.id, searched_sub.upper_category_id)

            print(*ctx.captured_queries, sep='\n')
            print("============================================")


class ProductTestCase(TransactionTestCase):
    def setUp(self) -> None:
        print("Set Up Test Models")
        saved_root_category = Category.objects.create(
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
        pass

    # TC 1 : 기본 상품 상태(ProductStatus.AVAILABLE) 정상 등록 여부 확인
    def test_product_default_status(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_product_default_status================")
            searched_product = Product.objects.get(name=SAMPLE_PRODUCT)
            self.assertEqual(ProductStatus.AVAILABLE, searched_product.status)
            print("============================================")


class ProductDetailsTestCase(TransactionTestCase):
    def setUp(self) -> None:
        with CaptureQueriesContext(connection) as ctx:
            print("Set Up Test Models")
            Category.objects.create(
                name=ROOT_CATEGORY,
            )

            product = Product.objects.create(
                name=SAMPLE_PRODUCT,
                short_description="short-description",
                category=Category.objects.get(name=ROOT_CATEGORY)
            )

            ProductDetails.objects.create(
                product=product,
                price=1000,
                currency=Currency.KRW,
                overview="제품 전반 설명",
                scent="향 정보",
                ingredients="제품 성분 정보",
                info="주요사양정보",
            )
            pass

    def test_product_details_with_product(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_product_details_exists================")

            """
            'SELECT 
                "product_details"."id", 
                "product_details"."created_at",
                "product_details"."modified_at",
                "product_details"."product_id",
                "product_details"."price",
                "product_details"."currency",
                "product_details"."overview",
                "product_details"."scent",
                "product_details"."ingredients",
                "product_details"."info",
                "product"."id",
                "product"."name", 
                "product"."short_description", 
                "product"."category_id", 
                "product"."status", 
                "product_category"."id", 
                "product_category"."created_at", 
                "product_category"."modified_at", 
                "product_category"."name", 
                "product_category"."upper_category_id", 
                "product_category"."status" 
             FROM 
                "product_details" 
             INNER JOIN 
                "product" 
             ON 
                ("product_details"."product_id" = "product"."id") 
             INNER JOIN 
                "product_category" 
             ON 
                ("product"."category_id" = "product_category"."id")
             WHERE 
                "product"."name" = \'product-sample\' 
             LIMIT 21', 'time': '0.000'
            """
            product_details = ProductDetails \
                .objects \
                .select_related('product') \
                .select_related('product__category') \
                .get(product__name=SAMPLE_PRODUCT)

            print(product_details.__str__())

            self.assertIsNotNone(product_details)
            self.assertIsNotNone(product_details.price)
            self.assertIsNotNone(product_details.currency)
            self.assertIsNotNone(product_details.info)

            print(*ctx.captured_queries, sep='\n')
            print("============================================")


class ProductReviewTestCase(TransactionTestCase):
    def setUp(self) -> None:
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("Set Up Test Models")
            Category.objects.create(
                name=ROOT_CATEGORY,
            )

            test_user: User = User.objects.create(
                name='tester',
                email='test@test.com',
                password=RAW_PASSWORD
            )

            test_product: Product = Product.objects.create(
                name=SAMPLE_PRODUCT,
                short_description="short-description",
                category=Category.objects.get(name=ROOT_CATEGORY)
            )

            ProductReview.objects.create(
                product=test_product,
                title=REVIEW_TITLE+'-01',
                details='details!!!',
                attached_image_url=None,
                user=test_user
            )

            ProductReview.objects.create(
                product=test_product,
                title=REVIEW_TITLE+'-02',
                details='details!!!',
                attached_image_url=None,
                user=test_user
            )

            print(*ctx.captured_queries, sep='\n')
            print("============================================")
            pass

    def test_product_review_list(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_product_review_list================")

            """
            'SELECT 
                "product_review"."id", 
                "product_review"."created_at", 
                "product_review"."modified_at", 
                "product_review"."product_id",
                 "product_review"."user_id", 
                 "product_review"."attached_image_url", 
                 "product_review"."title",
                 "product_review"."details",
                 "user"."id", "user"."password",
                 "user"."last_login",
                 "user"."created_at",
                 "user"."modified_at",
                 "user"."name",
                 "user"."email",
                 "user"."status",
                 "user"."type"
             FROM 
                "product_review" 
            INNER JOIN 
                "product" 
            ON 
                ("product_review"."product_id" = "product"."id")
            INNER JOIN 
                "user" 
            ON 
                ("product_review"."user_id" = "user"."id") 
            WHERE 
                "product"."name" = \'product-sample\'',  -- <- 이부분은 실제 Logic에서는 product_id 로 조건이 들어갈 예정.
            ORDER BY 
                "product_review"."created_at" ASC', 
            'time': '0.000'
            """
            review_list = ProductReview\
                .objects\
                .filter(product__name=SAMPLE_PRODUCT)\
                .select_related('user')\
                .order_by('created_at')

            print(serialize_product_review_list(review_list))
            self.assertEqual(2,len(review_list))
            self.assertEqual(REVIEW_TITLE+'-01', review_list[0].title)
            self.assertEqual(REVIEW_TITLE + '-02', review_list[1].title)
            print(*ctx.captured_queries, sep='\n')
