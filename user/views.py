import logging
import uuid

from django.contrib.auth import authenticate, logout
from django.core.cache import cache
from rest_framework.authentication import SessionAuthentication
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

            session_key = str(uuid.uuid4())
            cache.set(email, session_key)

            resp = {
                'session_key': session_key
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
            session_key = str(uuid.uuid4())
            cache.set(email, session_key)
            resp = {
                'session_key': session_key
            }
            return Response(resp)
        else:
            return Response(status=401)


class LogoutView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        response = logout(request)
        d = cache.get('marshall.s.lee@gmail.com')
        return Response(response)
