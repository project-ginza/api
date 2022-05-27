from rest_framework import serializers


class SignupRequestBodySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    email = serializers.EmailField()
    password = serializers.CharField()
    name = serializers.CharField()
    mobile = serializers.CharField(max_length=11)
    birthday = serializers.DateField()
    is_solar_calendar = serializers.BooleanField()
    agreed_with_mkt_info_subscription = serializers.BooleanField()

