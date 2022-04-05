from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from user.views import SignupView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view())
]
