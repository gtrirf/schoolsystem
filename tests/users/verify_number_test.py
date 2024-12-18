import pytest
from rest_framework import status
from faker import Faker
from apps.accounts.models import User, NumberVerification, RoleCodes

fake = Faker()

base_url = '/accounts/phone-number/'


@pytest.mark.django_db
def test_send_verification_to_new_number(api_client):
    url = base_url
    data = {'phone_number': fake.phone_number()[:15]}

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'message' in response.data
    assert response.data['message'] == 'Verification code is sent'
    assert NumberVerification.objects.filter(phone_number=data['phone_number']).exists()


@pytest.mark.django_db
def test_send_verification_to_registered_number(api_client, guest_user):
    url = base_url
    data = {'phone_number': guest_user.phone_number}

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'phone_number' in response.data
    assert response.data['phone_number'][0] == 'user with this phone number already exists.'


@pytest.mark.django_db
def test_send_verification_recent_code(api_client, verification_code_recent):
    url = base_url
    data = {'phone_number': verification_code_recent.phone_number}

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.data
    assert response.data['detail'] == 'You can only send a verification SMS once in one minute'


@pytest.mark.django_db
def test_send_verification_expired_code(api_client, verification_code_expired):
    url = base_url
    data = {'phone_number': verification_code_expired.phone_number}

    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'message' in response.data
    assert response.data['message'] == 'Verification code is sent'


