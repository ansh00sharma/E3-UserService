from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate

class SendOtpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = ["phone_number"]

    def validate_number(self,attrs):
        phone_number = attrs.get('phone_number')
        user = User.objects.get(phone_number=phone_number)
        if user is None:
            return
            
        return attrs
