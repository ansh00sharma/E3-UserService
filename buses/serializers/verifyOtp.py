from rest_framework import serializers
from users.models import User, UserProfile
from buses.serializers.userProfile import*
from django.shortcuts import get_object_or_404

class VerifyOtpSerializer(serializers.ModelSerializer):
    otp = serializers.CharField()
    class Meta:
        model = UserProfile
        fields = ["otp"]

    def verify_otp(self,attrs):
        phone_number = attrs.get('phone_number')
        otp = attrs.get("otp")
        try:
            user = get_object_or_404(User, phone_number=phone_number)
            # print("user", user)
            user_profile = get_object_or_404(UserProfile, user__email=user)
            # print("user_profile ", user_profile)
            if user_profile.otp == otp:
                user_profile.otp = None
                user_profile.save()
                return attrs
            else:
                return "OTP Not Matched"
        except:
            return "Not Found"
