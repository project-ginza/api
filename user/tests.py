import logging

from django.contrib.auth.hashers import check_password
from django.db import connection
from django.test import TransactionTestCase

# Create your tests here.
from user.models import User, UserTypeCategory, UserStatus
from django.test.utils import CaptureQueriesContext

logger = logging.getLogger('api')

EMAIL_VALUE_ERROR_TXT = 'Please enter your email.'
NAME_VALUE_ERROR_TXT = 'Please enter your name.'


# User Model Transaction Test
class UserTestCase(TransactionTestCase):
    def setUp(self):
        User.objects.create_user(
            name='tester',
            email='test@test.com',
            password='1234'
        )
        print("Set Up Test Models")

    # TC1 : 평문(raw-password)를 받아서 DB Insert시 Bcrypt로 해싱된 결과가 저장되어야 하고,
    # 동일한 평문에 대한 해시 검증(check_password)는 참이어야 한다.
    def test_user_password_encoding(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_user_password_encoding================")
            hashed_password = User.objects.get(name='tester').password
            print(*ctx.captured_queries, sep='\n')
            self.assertTrue(check_password('1234', hashed_password))
            print("============================================")

    # TC2 : 사용자 상태와 사용자 종류의 Default 값은 각각 Active와 Normal이 되어야 한다.
    def test_user_default_fields(self):
        with CaptureQueriesContext(connection) as ctx:
            print("============================================")
            print("=> test_user_default_fields================")
            searched_user = User.objects.get(name='tester')
            print(*ctx.captured_queries, sep='\n')
            print(searched_user.status.__str__() + "___" + searched_user.type.__str__())
            self.assertEqual(UserTypeCategory.NORMAL, searched_user.type)
            self.assertEqual(UserStatus.ACTIVE, searched_user.status)
            print("============================================")

    # TC3 : create_user시 email과 이름은 필수값이며 누락시 ValueError를 Raise 해야 한다.
    def test_create_user_validation_check(self):
        print("============================================")
        print("=> test_create_user_validation_check================")
        with self.assertRaisesMessage(ValueError, EMAIL_VALUE_ERROR_TXT):
            User.objects.create_user(None, 'invalid-email')
        with self.assertRaisesMessage(ValueError, NAME_VALUE_ERROR_TXT):
            User.objects.create_user('invalid-name@invalid.com', None)
        print("============================================")
