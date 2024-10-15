import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

base_url = '/accounts/logout/'


@pytest.mark.django_db
class TestLogoutView:

    @pytest.fixture
    def authenticated_client(self, api_client, create_roles, register_user):
        phone_number = '123123'
        user = register_user(phone_number)
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client, refresh

    def test_logout_successful(self, authenticated_client):
        api_client, refresh = authenticated_client

        url = base_url
        data = {
            'refresh': str(refresh),
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'] == 'Logged out successfully'

    def test_logout_invalid_token(self, authenticated_client):
        api_client, _ = authenticated_client

        url = base_url
        data = {
            'refresh': 'invalid_token',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    def test_logout_missing_token(self, authenticated_client):
        api_client, _ = authenticated_client

        url = base_url
        data = {}

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'refresh' in response.data
        assert response.data['refresh'] == ['This field is required.']