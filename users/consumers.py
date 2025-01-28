from channels.generic.websocket import AsyncWebsocketConsumer
import json
from rest_framework import status
import face_recognition
from asgiref.sync import sync_to_async
# from users.models import*
from PIL import Image
import io
from io import BytesIO

class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        await self.accept()
        print("WebSocket connection accepted")

    async def disconnect(self, close_code=9999):
        print(f"WebSocket disconnected: {close_code}")

    async def receive(self, bytes_data=None):
        try:
            if bytes_data:
                delimiter_index = bytes_data.find(b'\x00')
                email_bytes = bytes_data[:delimiter_index]

                email = email_bytes.decode('utf-8')
                image_data = bytes_data[delimiter_index + 1:]

                image = await self.convert_binary_to_image(image_data)

                if email and image:
                    res = await self.userLoginByImage(email,image)

                    if res==True:
                        await self.send(text_data=json.dumps({"status": status.HTTP_200_OK, "message":"Face ID Matched"}))
                    elif res==False:
                        await self.send(text_data=json.dumps({"status":status.HTTP_400_BAD_REQUEST, "message":"Face ID not Matched"}))
                    else:
                        await self.send(text_data=json.dumps({"status":status.HTTP_400_BAD_REQUEST, "message":"This UserId Doesn't Exist"}))
                else:
                    await self.send(text_data=json.dumps({"status": status.HTTP_400_BAD_REQUEST, "message": "Show a Valid Face ID"}))
            else:
                await self.send(text_data=json.dumps({"status": status.HTTP_400_BAD_REQUEST, "message": "Either Email or Face ID is Missing"}))
        except Exception as e:
            print("exception : ",str(e))
            await self.send(text_data=json.dumps({"status": status.HTTP_400_BAD_REQUEST, "message": "Internal Server Error"}))

    async def userLoginByImage(self,email,login_image):
        from users.models import UserProfile
        try:
            
            uploaded_face_image = await sync_to_async(face_recognition.load_image_file)(login_image)
            uploaded_face_encoding = face_recognition.face_encodings(uploaded_face_image)

            if not uploaded_face_encoding:
                return False

            userprofile = await sync_to_async(UserProfile.objects.get)(user__email=email)
            saved_full_face_image = userprofile.image_1

            if not saved_full_face_image:
                return False

            saved_full_face_image_stream = await self.convert_binary_to_image(saved_full_face_image)

            saved_face_image = await sync_to_async(face_recognition.load_image_file)(saved_full_face_image_stream)
    
            saved_face_image_encoding = face_recognition.face_encodings(saved_face_image)

            match = await sync_to_async(face_recognition.compare_faces)([saved_face_image_encoding[0]], uploaded_face_encoding[0], tolerance=0.5)
       
            print(match[0])
            if match[0]:
                
                return True
            else:
                return False
        except UserProfile.DoesNotExist:
            print("User does not exist")
            return None
        except Exception as e:
            print("exception : ",str(e))
            return False

    async def convert_binary_to_image(self, binary_data):
        try:
            # Convert the binary data to a BytesIO object
            image_stream = io.BytesIO(binary_data)
            image = Image.open(image_stream)

            # If the image format is not JPEG, convert it
            if image.format != 'JPEG':
                image = image.convert('RGB')

            # Return a file-like object (BytesIO) for further processing
            new_image_stream = io.BytesIO()
            image.save(new_image_stream, format="JPEG")
            new_image_stream.seek(0)  # Reset the stream position for reading

            return new_image_stream  # Return as file-like object (not PIL.Image)
        
        except Exception as e:
            print(f"Error converting binary to image: {e}")
            return None