import binascii
import json
import logging
import os

from django.contrib.auth import authenticate, logout
from ginza.redis import redis_conn
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User, UserProfile

logger = logging.getLogger('api')


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            email = data['email']
            password = data['password']
            name = data['name']

            mobile = data['mobile']
            date_of_birth = data['date_of_birth']
            is_solar_calendar = data['is_solar_calendar']
            agreed_with_mkt_info_subscription = data['agreed_with_mkt_info_subscription']

            user = User.objects.create_user(
                email=email,
                password=password,
                name=name
            )

            profile = UserProfile.objects.create(
                user=user,
                mobile=mobile,
                birthday=date_of_birth,
                is_solar_calendar=is_solar_calendar,
                agreed_with_mkt_info_subscription=agreed_with_mkt_info_subscription,
            )

            token = binascii.hexlify(os.urandom(20)).decode()
            _dict = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
            redis_conn.set(token, json.dumps(_dict))

            resp = {
                'token': token
            }
            return Response(resp)

        except Exception as e:
            logger.error('An exception occurred while authentication '.format(e))
            raise e


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            token = binascii.hexlify(os.urandom(20)).decode()
            _dict = {
                'id': user.id,
                'email': user.email,
                'name': user.name
            }
            redis_conn.set(token, json.dumps(_dict))

            resp = {
                'session_key': token
            }
            return Response(resp)
        else:
            return Response(status=401)


class LogoutView(APIView):
    def post(self, request):
        response = logout(request)
        return Response(response)
