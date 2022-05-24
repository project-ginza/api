from rest_framework import serializers
from user.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'
        # fields = ('email, password, name',)


class UserProfileSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=11)
    birthday = serializers.DateField()
    is_solar_calendar = serializers.BooleanField()
    agreed_with_mkt_info_subscription = serializers.BooleanField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        # fields = ('mobile', 'birthday', 'is_solar_calendar', 'agreed_with_mkt_info_subscription',)


class SignupRequestBodySerializer(UserSerializer, UserProfileSerializer):
    def __init__(self):
        super(SignupRequestBodySerializer, self).__init__()
