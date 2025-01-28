from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from buses.serializers.userRegister import UserRegistrationSerializer
from buses.serializers.userLogin import UserLoginSerializer
from buses.serializers.sendOtp import SendOtpSerializer
from buses.serializers.verifyOtp import VerifyOtpSerializer
from buses.serializers.userProfile import*
from rest_framework_simplejwt.tokens import RefreshToken
from buses.utils.sendOtp import SendOtp
from django.shortcuts import get_object_or_404
import random
from buses.utils.serializerErrorFormatter import format_serializer_errors
from buses.serializers.responseRenderer import*
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import*
from django.db.models.signals import post_save
from django.dispatch import receiver
import face_recognition
from PIL import Image
import io
from io import BytesIO

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def userRegisteration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() 
        token = get_tokens_for_user(user)
        return Response({"token":token,"message":'User Registered Successfully',"status":status.HTTP_201_CREATED})
    else:
        formatted_error = format_serializer_errors(serializer.errors)
        print("Invalid serializer data:",formatted_error)
        return Response({"message": formatted_error['message'], "status": status.HTTP_400_BAD_REQUEST})
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@api_view(['POST'])
def userLogin(request):
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.get_user(request.data)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({"token":token,"message":'Login Successfully',"status":status.HTTP_200_OK})
        else:
            return Response({"message": "Email or Password is not Valid", "status": status.HTTP_400_BAD_REQUEST})
    else:
        formatted_error = format_serializer_errors(serializer.errors)
        print("Invalid serializer data:",formatted_error)
        return Response({"message": formatted_error['message'], "status": status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def sendOtpForLogin(request):
    data = request.data
    serializer = SendOtpSerializer(data=request.data)
    # print(data['phone_number'])
    if serializer.is_valid():
            user = serializer.validate_number(request.data)
            if user:
                otp = str(random.randint(100000, 999999))
                print(user)
                user_profile = UserProfile.objects.get(user__phone_number=user['phone_number'])
                user_profile.otp = otp
                user_profile.save()

                messsage = "Mere Balka ka Maa Tanne I love You. Motalli......"
                otp_handler = SendOtp(user['phone_number'],otp,messsage)
                otp_handler.sendOtpOnNumber()
                return Response({"message": "OTP for Login is send to your Registered Number", "status": status.HTTP_200_OK})
            else:
                return Response({"message": "This Number is not Registered", "status": status.HTTP_400_BAD_REQUEST})
    else:
        return Response({"message": "Enter Your Registered phone number", "status": status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def verifyOtpForLogin(request):
    serializer = VerifyOtpSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.verify_otp(request.data)    
        if user == request.data:
            return Response({"message":'Login Successfully',"status":status.HTTP_200_OK})
        elif user == "OTP Not Matched":
            return Response({"message":'Invalid OTP',"status": status.HTTP_400_BAD_REQUEST})
        else:
            return Response({"message":'User not Found',"status": status.HTTP_400_BAD_REQUEST})
    else:
        return Response({"message": "Enter Your Registered phone number", "status": status.HTTP_400_BAD_REQUEST})


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

    
    