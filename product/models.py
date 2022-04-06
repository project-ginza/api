from common.models import BaseModel
from django.db import models
from user.models import User


class CategoryStatus(models.IntegerChoices):
    AVAILABLE = 0,
    NOT_AVAILABLE = 1


class Category(BaseModel):

    # 카테고리명
    name = models.CharField(
        max_length=255,
        null=False,
        default=None
    )

    # 상위 카테고리 id
    upper_category_id = models.BigIntegerField(
        null=True,
        default=None
    )

    # 카테고리 상태 (활성, 비활성)
    status = models.IntegerField(choices=CategoryStatus.choices, default=CategoryStatus.AVAILABLE)

    class Meta:
        db_table = 'product_category'


class ProductStatus(models.IntegerChoices):
    AVAILABLE = 0
    NOT_AVAILABLE = 1


class Product(models.Model):
    class Meta:
        db_table = 'product'

    # 상품명
    name = models.CharField(
        max_length=100,
        null=False,
        default=None
    )

    # 상품에 대한 간단한 설명.
    short_description = models.CharField(
        max_length=50,
        null=False,
        default=None
    )

    # 제품 카테고리
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    # 상품 상태
    status = models.IntegerField(choices=ProductStatus.choices, default=ProductStatus.AVAILABLE)


# 상품 이미지 저장 URL 보관 테이블
class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    image_url = models.CharField(
        max_length=255,
        null=False,
        default=None
    )

    class Meta:
        db_table = 'product_image'


class Currency(models.IntegerChoices):
    KRW = 0


# 상품 상세 정보 테이블
class ProductDetails(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    # 가격
    price = models.DecimalField(
        decimal_places=2,
        max_digits=9,
        null=False,
        default=None
    )

    # 가격 통화 정보
    currency = models.IntegerField(default=Currency.KRW)

    # 제품 전반 설명
    overview = models.TextField(
        default=None
    )

    # 향 정보
    scent = models.TextField(
        default=None
    )

    # 제품 성분 정보
    ingredients = models.TextField(
        default=None
    )

    # 제품 주요 사양 정보
    info = models.TextField(
        default=None
    )

    class Meta:
        db_table = 'product_details'
        verbose_name = 'product_details'
        verbose_name_plural = 'product_details'


# 제품 리뷰 정보를 담는 테이블
class ProductReview(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    # 작성자 외래키
    # 사용자가 삭제되어도 레코드에는 영향이 없다.
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )

    # 첨부 이미지 URL.
    attached_image_url = models.CharField(
        max_length=255,
        null=True,
        default=None
    )

    # 제목
    title = models.CharField(
        max_length=100,
        null=False,
        default=None
    )

    # 본문
    details = models.TextField(
        null=False,
        default=None
    )

    class Meta:
        db_table = 'product_review'
