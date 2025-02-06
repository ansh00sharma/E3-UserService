from .models import*
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta

from buses.serializers.userRegister import UserRegistrationSerializer
from buses.serializers.userLogin import UserLoginSerializer
from buses.serializers.sendOtp import SendOtpSerializer
from buses.serializers.verifyOtp import VerifyOtpSerializer
from buses.serializers.userProfile import*
from buses.utils.sendOtp import SendOtp
from buses.utils.serializerErrorFormatter import format_serializer_errors
from buses.serializers.responseRenderer import*
from buses.utils.getClientDeviceInfo import*
from buses.utils.getClientIp import*
from buses.utils.userLogs import log_user_action

import io
import random
from io import BytesIO
from PIL import Image
import face_recognition



def get_tokens_for_user(request,user):
    refresh = RefreshToken.for_user(user) # using user uuid for creating token

    ip_address = get_client_ip(request)
    device_info = get_client_device_info(request)

    # Save refresh token to the database with device and IP info
    Token.objects.create(
        user=user,
        token=str(refresh),
        device_info=device_info,
        ip_address=ip_address,
        expired_at=now() + timedelta(days=15)  # assuming a 15-day expiry
    )
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def userRegisteration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() 
        log_status = log_user_action(request,user,"Your Account was registered Successfully.")
        return Response({"message":'User Registered Successfully',"status":status.HTTP_201_CREATED,"logged":log_status})
    else:
        formatted_error = format_serializer_errors(serializer.errors)
        print("Invalid serializer data:",formatted_error)
        return Response({"message": formatted_error['message'], "status": status.HTTP_400_BAD_REQUEST})
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@api_view(['POST'])
def userLoginByEmail(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.get_user(request.data)
        if user is not None:
            # create UserService token for user
            token = get_tokens_for_user(request,user)
        
            log_status = log_user_action(request,user,"You Logged In via your Registered Email Successfully.")
            response = Response({"access_token":token['access'],"message":'Login Successfully',"status":status.HTTP_200_OK, "logged":log_status})
            response.set_cookie(key='refresh_token',value=token['refresh'],httponly=True,secure=True,samesite='Strict',max_age=15 * 24 * 60 * 60)  # 15 days in seconds)
            return response
        else:
            return Response({"message": "Email or Password is not Valid", "status": status.HTTP_400_BAD_REQUEST})
    else:
        formatted_error = format_serializer_errors(serializer.errors)
        return Response({"message": formatted_error['message'], "status": status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def userLoginByImage(request):
    
    try:
        email = request.data.get('email')
        login_image = request.FILES.get('image')  # Use FILES to handle uploaded file
    
        if not email or not login_image:
            return Response({"message": "Email id or Image not Captured Properly", "status": status.HTTP_200_OK})

        uploaded_face_image = face_recognition.load_image_file(login_image)
        uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)
    
        if not uploaded_face_encoding:
            return Response({"message":"Unable to Detect Face", "status": status.HTTP_400_BAD_REQUEST})

        userprofile = UserProfile.objects.get(user__email=email)
        saved_full_face_image = userprofile.image_1

        if not saved_full_face_image:
            return Response({"message": "Unable to Detect Face (Server Side)", "status": status.HTTP_400_BAD_REQUEST})

        saved_full_face_image = convert_binary_to_image(saved_full_face_image)
        saved_full_face_image_file = BytesIO()
        saved_full_face_image.save(saved_full_face_image_file, format="JPEG")
        saved_full_face_image_file.seek(0)

        saved_face_image = face_recognition.load_image_file(saved_full_face_image_file)
        saved_face_image_encoding = face_recognition.face_encodings(saved_face_image)

        match = face_recognition.compare_faces([saved_face_image_encoding[0]],uploaded_face_encoding[0],tolerance=0.5)
        if match[0]:
            return Response({"message":"Face ID Matched","status":status.HTTP_200_OK})
        else:
            return Response({"message":"Face ID not Matched","status":status.HTTP_400_BAD_REQUEST})
    except UserProfile.DoesNotExist:
        return Response({"message":'This Email ID is not Registered',"status":status.HTTP_404_NOT_FOUND})
    except Exception as e:
        return Response({"message": str(e), "status": status.HTTP_400_BAD_REQUEST})

    
@api_view(['POST'])
def UserLoginByContact(request):
    serializer = SendOtpSerializer(data=request.data)
    if serializer.is_valid():
            user = serializer.validate_number(request.data)
            if user:
                otp = str(random.randint(100000, 999999))
                user_profile = UserProfile.objects.get(user__phone_number=user['phone_number'])
                user_profile.otp = otp
                user_profile.save()

                messsage = "Your OTP for logging into GenAi"
                otp_handler = SendOtp(user['phone_number'],otp,messsage)
                otp_handler.sendOtpOnNumber()
                log_status = log_user_action(request,user.uuid,"Otp for LogIn is send to your Registered Number.")
                return Response({"message": "OTP for Login is send to your Registered Number", "status": status.HTTP_200_OK,"logged":log_status})
            else:
                return Response({"message": "This Number is not Registered", "status": status.HTTP_400_BAD_REQUEST})
    else:
        return Response({"message": "Enter Your Registered phone number", "status": status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def verifyOtpForLogin(request):
    serializer = VerifyOtpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.verify_otp(request.data)    
        if user == "OTP Not Matched":
            log_status = log_user_action(request,user.uuid,"Tried to LogIn but Otp Didn't Match.")
            return Response({"message":'Invalid OTP',"status": status.HTTP_400_BAD_REQUEST,"logged":log_status})
        
        elif user == "Not Found":
            return Response({"message":'User not Found',"status": status.HTTP_400_BAD_REQUEST})
        
        else:
            # create token for user
            token = get_tokens_for_user(user)
            log_status = log_user_action(request,user.uuid,"You Logged In via Registered Number Successfully.")
            return Response({"token":token,"message":'Login Successfully',"status":status.HTTP_200_OK,"logged":log_status})
            
    else:
        return Response({"message": "Enter Your Registered phone number", "status": status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userLogout(request):
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token is None:
            return Response({"message": "Refresh token is required.","status":status.HTTP_400_BAD_REQUEST})

        token = RefreshToken(refresh_token)
        token.blacklist()

        Token.objects.filter(token=refresh_token, user=request.user).update(is_blacklisted=True)
        return Response({"message": "User Logged out Successfully.","status":status.HTTP_205_RESET_CONTENT})
    
    except TokenError:
        return Response({"message": "Invalid or expired refresh token.","status":status.HTTP_400_BAD_REQUEST}, )
    except Exception as e:
        return Response({"message": str(e),"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
    
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


@api_view(['POST'])
def userUpdateProfile(request):
    print(request.data)
    return Response({"message":'Profile Updated Successfully',"status":status.HTTP_200_OK})

def convert_binary_to_image(binary_data):
    try:
        # Create an in-memory binary stream from the binary data
        image_stream = io.BytesIO(binary_data)
        
        # Open the stream as an image
        image = Image.open(image_stream)

        # Ensure the image is in JPEG format
        if image.format != 'JPEG':
            image = image.convert('RGB')  # Convert to RGB if required
        return image
    except Exception as e:
        print(f"Error converting binary to image: {e}")
        return None
    

    