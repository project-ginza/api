import binascii
import json
import logging
import os
import requests

from django.contrib.auth import authenticate, logout
from django.conf import settings
from django.shortcuts import redirect
from ginza.redis import redis_conn
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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
                'token': token
            }
            return Response(resp)
        else:
            return Response(status=401)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        key = request.auth
        redis_conn.delete(key)
        response = logout(request)
        return Response(response)


# reference: https://velog.io/@junsikchoi/Django%EB%A1%9C-%EC%B9%B4%EC%B9%B4%EC%98%A4-%EC%86%8C%EC%85%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8%EC%9D%84-%ED%95%B4%EB%B3%B4%EC%9E%90
class KakaoOAuthLoginCallbackView(APIView):
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirection_uri': settings.KAKAO_REDIRECT_URI,
            'code': auth_code
        }
        token_response = requests.post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
        response = {
            'user_info': user_info_response.json()
        }
        return Response(response)


class KakaoOAuthLoginView(APIView):
    def get(self, request):
        client_id = settings.KAKAO_REST_API_KEY
        redirect_url = settings.KAKAO_REDIRECT_URI
        url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".\
            format(client_id, redirect_url)
        res = redirect(url)
        return res
