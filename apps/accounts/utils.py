from django.conf import settings
import random
import string
from twilio.rest import Client
from apps.accounts.models import NumberVerification
from rest_framework.response import Response
from rest_framework import status


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))


def send_verification_sms(to_phone_number, message_body):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=to_phone_number
        )
        print(f"Message SID: {message.sid}")

    except Exception as e:
        print(f"Exception occurred: {e}")


def create_verification(phone_number, verification_code):
    NumberVerification.objects.create(
        phone_number=phone_number,
        verification_code=verification_code,
    )
    message = f'Your verification code is {verification_code}'
    try:
        send_verification_sms(phone_number, message)
    except Exception as e:
        return Response(
            {'error': "Failed to send verification SMS"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return Response(
        {'message': 'Verification code is sent'},
        status=status.HTTP_200_OK
    )
