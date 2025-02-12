from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ["email","password"]

    def get_user(self,data):  
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if user is None:
            return
        return user
    
    def format_user(self,uuid):
        user = get_object_or_404(User, uuid=uuid)  # If UUID is in the primary key
        user_data = {
            "email": user.email,
            "name": user.name,
            "phone_number": user.phone_number,
            "gender": user.gender,
        }
        return user_data
    
        
               