from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, logout
from user.models import User, UserProfile


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user_id = data['user_id']
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
                user_id=user_id,
                name=name
            )

            user.save()

            profile = UserProfile.objects.create(
                user=user,
                mobile=mobile,
                birthday=date_of_birth,
                is_solar_calendar=is_solar_calendar,
                agreed_with_mkt_info_subscription=agreed_with_mkt_info_subscription,
            )

            profile.save()

            token = Token.objects.create(user=user)

            resp = {
                'token': token.key
            }
            return Response(resp)

        except Exception as e:
            resp = {
                'msg': e
            }
            raise

