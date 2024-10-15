import pytest
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import NumberVerification
from apps.accounts.serializers import VerifyNumberSerializer


@pytest.mark.django_db
class TestVerifySmsView:

    def create_verification(self, phone_number, verification_code, is_verified=False):
        return NumberVerification.objects.create(
            phone_number=phone_number,
            verification_code=verification_code,
            is_verified=is_verified,
            created_at=timezone.now()
        )

    def test_successful_verification(self, api_client):
        phone_number = '1234567890'
        verification_code = '123456'
        self.create_verification(phone_number, verification_code)

        response = api_client.post(
            '/accounts/verify-sms/',
            {'phone_number': phone_number, 'verification_code': verification_code},
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Phone number verified successfully."
        assert NumberVerification.objects.get(phone_number=phone_number).is_verified is True

    def test_expired_verification_code(self, api_client):
        phone_number = '1234567890'
        verification_code = '123456'
        verification = self.create_verification(phone_number, verification_code)
        verification.created_at = timezone.now() - timedelta(minutes=2)
        verification.save()

        response = api_client.post(
            '/accounts/verify-sms/',
            {'phone_number': phone_number, 'verification_code': verification_code},
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Verification code has expired, get a new one'

    def test_invalid_verification_code_or_phone_number(self, api_client):
        phone_number = '1234567890'
        verification_code = '123456'
        self.create_verification(phone_number, verification_code)

        response = api_client.post(
            '/accounts/verify-sms/',
            {'phone_number': phone_number, 'verification_code': '654321'},
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid verification code or phone number.'

        response = api_client.post(
            '/accounts/verify-sms/',
            {'phone_number': '0987654321', 'verification_code': verification_code},
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid verification code or phone number.'

    def test_invalid_input_data(self, api_client):
        response = api_client.post(
            '/accounts/verify-sms/',
            {'verification_code': '123456'},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'phone_number' in response.data

        response = api_client.post(
            '/accounts/verify-sms/',
            {'phone_number': '1234567890'},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'verification_code' in response.data
