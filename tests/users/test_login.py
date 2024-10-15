import pytest
from rest_framework import status

base_url = '/accounts/login/'


@pytest.mark.django_db
class TestLoginView:
    def test_login_successful(self, api_client, create_roles, register_user):
        phone_number = '123123'
        register_user(phone_number)
        url = base_url
        data = {
            'phone_number': phone_number,
            'password': 'password123'
        }
        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Login successful'
        assert 'access_token' in response.data
        assert 'refresh_token' in response.data

    def test_login_phone_number_or_password_incorrect(self, api_client, create_roles, create_verified_number):
        phone_number = '123123'
        create_verified_number(phone_number)
        url = base_url
        data = {
            'phone_number': phone_number,
            'password': 'password',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid Phone Number or password'

        data = {
            'phone_number': '321321',
            'password': 'password'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Invalid Phone Number or password'

    def test_login_without_verified_number(self, api_client):
        phone_number = '123123'

        url = base_url
        data = {
            'phone_number': phone_number,
            'password': 'password123'
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Invalid Phone Number or password"
