from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView


class GinzaCommonAuthAPIView(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class GinzaAdminAuthAPIView(APIView):
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAdminUser, ]
