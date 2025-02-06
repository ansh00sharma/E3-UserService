from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.models import model_to_dict

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
    
        
               