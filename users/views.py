import rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from buses.serializers.userRegister import UserRegistrationSerializer
from buses.serializers.userLogin import UserLoginSerializer
from buses.serializers.userProfile import*
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from buses.serializers.responseRenderer import*
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def userRegisteration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save() 
        token = get_tokens_for_user(user)
        return Response({"token":token,"message":'User Registered Successfully',"status":status.HTTP_201_CREATED})

@api_view(['POST'])
def userLogin(request):
    serializer = UserLoginSerializer(data=request.data)
    user = serializer.is_valid(raise_exception=True)
    if user is not None:
        user = serializer.get_user(request.data)
        token = get_tokens_for_user(user)
        return Response({"token":token,"message":'Login Successfully',"status":status.HTTP_200_OK})
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userProfile(request):
    serializer = UserProfileSerializer(request.user)
    if serializer is not None:
        return Response({"data": serializer.data,"status":status.HTTP_200_OK })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    print("request.user : ", request.user)
    print("request.data : ", request.data)
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    if serializer.is_valid(raise_exception=True):
        return Response({"message":'Password Changed Successfully',"status":status.HTTP_200_OK})

@api_view(['POST'])
def sendresetPassword(request):
    serializer = UserSendResetPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        return Response({"message":'Password Reset Link is Send to your Registered Email',"status":status.HTTP_200_OK})

@api_view(['POST'])
def resetPassword(request,uid,token):
    serializer = UserResetPasswordSerializer(data=request.data, context={'uid':uid,'token':token})
    if serializer.is_valid(raise_exception=True):
        return Response({"message":'Password Reset Successfully',"status":status.HTTP_200_OK})
