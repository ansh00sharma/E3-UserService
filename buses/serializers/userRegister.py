from rest_framework import serializers
from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email','name','phone_number','gender','password','confirm_password']

    def validate(self,data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password's Doesn't Match")
       
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)