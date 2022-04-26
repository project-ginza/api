from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView


class GinzaCommonAuthAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class GinzaAdminAuthAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]
