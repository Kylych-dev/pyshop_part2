from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt, datetime
from datetime import datetime, timedelta

from django.conf import settings


from .serializers import CustomUserSerializer
from accounts.models import CustomUser, RefreshToken
from utils.custom_logger import log_error, log_warning
from utils.auth import (
    generate_access_token, 
    generate_refresh_token
    )



class RegisterView(viewsets.ViewSet):
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        operation_description="Создание нового пользователя.",
        operation_summary="Создание нового пользователя",
        operation_id="register_user",
        tags=["Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Пароль пользователя')
            },
        ),
        responses={
            201: openapi.Response(description="OK - Регистрация прошла успешно."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def register(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                validated_data = serializer.validated_data
                email = validated_data.get("email")

                existing_user = CustomUser.objects.filter(email=email).exists()
                if existing_user:
                    log_warning(self, 'уже существует')
                    return Response(
                        data={"error": "Пользователь с таким email уже существует"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user = CustomUser.objects.create_user(
                    email=email, 
                    password=validated_data.get("password")
                    )
                user.set_password(validated_data.get("password"))
                user.save()
                return Response(
                    serializer.data, 
                    status=status.HTTP_201_CREATED
                    )
            except Exception as ex:
                log_error(self, ex)
                return Response(
                    data={"error": f"User creation failed: {str(ex)}"},
                    status=status.HTTP_400_BAD_REQUEST,)
        else:
            log_error(self, ex)
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
                )



class AuthenticationView(viewsets.ViewSet):
    @swagger_auto_schema(
        operation_description="Авторизация пользователя для получения токена.",
        operation_summary="Авторизация пользователя для получения токена",
        operation_id="login_user",
        tags=["Authentication"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email пользователя'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Пароль пользователя')
            },
        ),   
        responses={
            200: openapi.Response(description="OK - Авторизация пользователя прошла успешно."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not email or not password:
            return Response(
                data={"error": "Email and password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password.")
        
        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)


        response = Response(
            data={
                "jwt": access_token,
                "refresh_token": refresh_token,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie('jwt', access_token)
        return response
    
    @swagger_auto_schema(
        operation_description="Выход для удаления токена.",
        operation_summary="Выход для удаления токена",
        operation_id="logout_user",
        tags=["Authentication"],
        responses={
            201: openapi.Response(description="OK - Выход пользователя прошел успешно."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
        },
    )
    def logout(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    



class UserView(APIView):

    @swagger_auto_schema(
        operation_description="Получение данных пользователя.",
        operation_summary="Получение данных пользователя",
        operation_id="retrieve_user",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Новый email пользователя'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Новое имя пользователя')
            },
        ),   
        responses={
            200: openapi.Response(description="OK - Данные пользователя успешно обновлены."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = CustomUser.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed('User not found!')
        
        user = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Обновление данных пользователя.",
        operation_summary="Обновление данных пользователя",
        operation_id="update_user",
        tags=["User"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'username'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Новый email пользователя'),
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Новое имя пользователя')
            },
        ),   
        responses={
            200: openapi.Response(description="OK - Данные пользователя успешно обновлены."),
            400: openapi.Response(description="Bad Request - Неверный запрос."),
            404: openapi.Response(description="Not Found - Пользователь не найден"),
        },
    )
    def put(self, request):
    
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
        user = CustomUser.objects.get(id=user_id)

        data = request.data
        if 'email' in data:
            user.email = data['email']
        if 'username' in data:
            user.username = data['username']

        user.save()

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    


'''
    
Retrieving Personal Information

Endpoint: /api/me/
Method: GET
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Response: {"id": 1, "username": "", "email": "user@example.com"}

curl -X GET http://localhost:8000/api/me/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA"





Updating Personal Information

Endpoint: /api/me/
Method: PUT
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Body: {"username": "John Smith"}
Response: {"id": 1, "username": "John Smith", "email": "user@example.com"}

curl -X PUT http://localhost:8000/api/me/ -d '{"email": "newuser@example.com"}' -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA"
    
'''