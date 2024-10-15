import pytest
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from tests.conftest import create_roles


@pytest.mark.django_db
class TestCompleteRegisterView:

    def test_successful_registration(self, api_client, create_roles, create_verified_number):
        phone_number = '1234567890'
        create_verified_number(phone_number)

        data = {
            'phone_number': phone_number,
            'username': 'testuser',
            'password': 'password123',
            'password_confirm': 'password123'
        }

        response = api_client.post('/accounts/register/', data, format='json')
        print(response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['message'] == "Registration successful."
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_phone_number_not_verified(self, api_client):
        phone_number = '1234567890'
        data = {
            'phone_number': phone_number,
            'username': 'testuser',
            'password': 'password123'
        }

        response = api_client.post('/accounts/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Phone number is not verified or not found."

    def test_expired_verification(self, api_client, create_verified_number):
        phone_number = '1234567890'
        verification = create_verified_number(phone_number)
        verification.created_at = timezone.now() - timedelta(minutes=6)
        verification.save()

        data = {
            'phone_number': phone_number,
            'username': 'testuser',
            'password': 'password123'
        }

        response = api_client.post('/accounts/register/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Phone number verification expired. Please verify again."

    def test_invalid_input_data(self, api_client, create_verified_number):
        phone_number = '1234567890'
        create_verified_number(phone_number)

        data = {
            'phone_number': phone_number,
            'password': ''
        }

        response = api_client.post('/accounts/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'message' in response.data
        assert response.data['message'] == 'Something went wrong!'
