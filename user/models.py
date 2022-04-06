from common.models import BaseModel
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# 사용자 상태 enum
class UserStatus(models.IntegerChoices):
    ACTIVE = 0   # 일반
    DORMANT = 1  # 휴면
    BLOCKED = 2  # 이용제한
    DELETED = 3  # 삭제


# 사용자 등급
class UserTypeCategory(models.IntegerChoices):
    NORMAL = 0  # 일반 회원
    SELLER = 1  # 판매자 회원
    OPERATOR = 2   # 운영자
    ADMIN = 3      # 관리자
    SUPERUSER = 4  # 최고관리자


class UserManager(BaseUserManager):
    def create_user(self, user_id, email, name, password=None):
        if not user_id:
            raise ValueError('Please enter your ID.')

        if not email:
            raise ValueError('Please enter your email.')

        if not name:
            raise ValueError('Please enter your name.')

        user = self.model(
            user_id=user_id,
            email=self.normalize_email(email),
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, email, name, password):
        user = self.create_user(
            user_id=user_id,
            email=email,
            name=name,
            password=password
        )
        user.type = UserTypeCategory.SUPERUSER
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel, PermissionsMixin):

    class Meta:
        db_table = 'user'

    user_id = models.CharField(
        max_length=100,
        null=False,
        default=None
    )

    name = models.CharField(
        max_length=100,
        null=False,
        default=None
    )

    email = models.EmailField(
        max_length=100,
        unique=True,
    )

    # 현재 사용자 상태
    status = models.IntegerField(
        null=False,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE
    )

    # 사용자 종류
    type = models.IntegerField(
        null=False,
        choices=UserTypeCategory.choices,
        default=UserTypeCategory.NORMAL
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_id']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.type >= UserTypeCategory.OPERATOR

    @property
    def is_admin(self):
        return self.type >= UserTypeCategory.ADMIN

    @property
    def is_superuser(self):
        return self.type == UserTypeCategory.SUPERUSER


class UserProfile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # 휴대폰 번호
    mobile = models.CharField(
        max_length=11,
        null=False,
        default=None
    )

    # 생년월일
    birthday = models.DateField(default=None)

    # 양력 여부. True면 양력, False면 음력.
    is_solar_calendar = models.BooleanField(default=True)

    # 마케팅 정보 수신 동의 여부
    agreed_with_mkt_info_subscription = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_profile'


# 주소 정보를 담은 테이블. 사용자 별 복수개의 주소를 등록할 수 있으므로 별도의 테이블로 떼어냈음.
class Address(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    # 주 배송지 여부.
    # 특정 회원에 대해 등록된 주소가 복수개인 경우, is_primary = True를 만족하는 레코드는 하나만이어야 한다.
    is_primary = models.BooleanField(
        default=True
    )

    address = models.CharField(
        max_length=100,
        null=False,
        default=None
    )

    # 주소에 대한 별칭 (예: 우리 집, 직장 등등)
    alias = models.CharField(
        max_length=20,
        null=True,
        default=None
    )

    class Meta:
        db_table = 'address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
