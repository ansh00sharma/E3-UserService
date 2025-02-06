import os
from twilio.rest import Client


class SendOtp:

    phone_number = None
    otp = None
    message = None

    def __init__(self,phone_number,otp,message=None):
        self.phone_number = phone_number
        self.otp = otp
        self.message = message

    def sendOtpOnNumber(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH')
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"{self.message} is {self.otp}",
            from_=os.getenv('TWILIO_NUMBER'),
            to=f'+91{self.phone_number}'
        )

        print(message.body)