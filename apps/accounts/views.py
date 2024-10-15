from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    UserPhoneNumberSerializer,
    VerifyNumberSerializer,
    UserPhoneNumberSerializer,
    LoginSerializer, UserRegistrationSerializer, LogoutSerializer
)
from .models import NumberVerification
from .utils import generate_verification_code, send_verification_sms, send_verification_sms_with_error_handling
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample


class PhoneNumberView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserPhoneNumberSerializer,
        responses={200: UserPhoneNumberSerializer},
    )
    def post(self, request):
        serializer = UserPhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = generate_verification_code()
            verification = NumberVerification.objects.filter(phone_number=phone_number).first()
            current_time = timezone.now()
            if User.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {'detail': "There is already a registered user for this number"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif verification:
                five_minute_expiration = verification.created_at + timedelta(minutes=5)
                if current_time > five_minute_expiration:
                    verification.delete()
                    NumberVerification.objects.create(
                        phone_number=phone_number,
                        verification_code=verification_code,
                    )
                    message = f'Your verification code is {verification_code}'
                    if not send_verification_sms_with_error_handling(phone_number, message):
                        return Response(
                            {'error': "error sending sms"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    return Response(
                        {'message': 'Verification code is sent'},
                        status=status.HTTP_200_OK
                    )
                elif verification.is_expired():
                    verification.verification_code = verification_code
                    verification.created_at = current_time
                    verification.save()

                    message = f'your Verification code is {verification_code}'
                    if not send_verification_sms_with_error_handling(phone_number, message):
                        return Response(
                            {'error': "error sending sms"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                    return Response(
                        {'message': 'New Verification code sent'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'detail': 'You can only send a verification SMS once in one minute'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                NumberVerification.objects.create(
                    phone_number=phone_number,
                    verification_code=verification_code,
                )
                message = f'Your verification code is {verification_code}'
                if not send_verification_sms_with_error_handling(phone_number, message):
                    return Response(
                        {'error': "error sending sms"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                return Response(
                    {'message': 'Verification code is sent'},
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifySmsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=VerifyNumberSerializer,
        responses={200: VerifyNumberSerializer},
    )
    def post(self, request):
        expiration_time = timezone.now() - timedelta(minutes=5)
        NumberVerification.objects.filter(created_at__lt=expiration_time).delete()

        serializer = VerifyNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            try:
                verification = NumberVerification.objects.get(
                    phone_number=phone_number,
                    verification_code=verification_code,
                )
                if verification.is_expired():
                    verification.delete()
                    return Response(
                        {
                            'error': 'Verification code has expired, get a new one'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                verification.is_verified = True
                verification.save()
                return Response(
                    {"message": "Phone number verified successfully."},
                    status=status.HTTP_200_OK
                )
            except NumberVerification.DoesNotExist:
                return Response(
                    {"error": "Invalid verification code or phone number."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={200: UserRegistrationSerializer},
    )
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification = NumberVerification.objects.filter(phone_number=phone_number, is_verified=True).first()
        if not verification:
            return Response(
                {"error": "Phone number is not verified or not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        five_minute_expiration = verification.created_at + timedelta(minutes=5)
        if timezone.now() > five_minute_expiration:
            verification.delete()
            return Response(
                {"error": "Phone number verification expired. Please verify again."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            verification.delete()

            return Response(
                {
                    "message": "Registration successful.",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'message': 'Something went wrong!'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            user = authenticate(phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response(
                    {
                        'message': 'Login successful',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'error': "Invalid Phone Number or password"
                 },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @extend_schema(
        request=LogoutSerializer,
        responses={
            200: OpenApiResponse(
                description='Logged out successfully',
                examples=[
                    OpenApiExample(
                        'Success',
                        value={'detail': 'Logged out successfully'},
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Invalid request or token',
                examples=[
                    OpenApiExample(
                        'Error',
                        value={'error': 'Invalid token or other error message'},
                    )
                ]
            ),
        },
        operation_id='logout',
        summary='Logout the user',
    )
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(
                {
                    'detail': 'Logged out successfully'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
