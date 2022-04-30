from django.urls import path
from user.views import SignupView, LoginView, LogoutView
from util.common import API_COMMON_PATH

urlpatterns = [
    path(API_COMMON_PATH + 'auth/signup', SignupView.as_view()),
    path(API_COMMON_PATH + 'auth/login', LoginView.as_view()),
    path(API_COMMON_PATH + 'auth/logout', LogoutView.as_view())
]

