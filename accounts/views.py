from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt, datetime
from datetime import datetime, timedelta

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



# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = CustomUser.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('User not found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')

#         payload = {
#             'id': user.id,
#             'exp': datetime.utcnow() + timedelta(minutes=60),
#             'iat': datetime.utcnow()
#         }

#         # token = jwt.encode(payload, 'secret', algorithm='HS256')
#         token = jwt.encode(payload, 'secret', algorithm='HS256')


#         response = Response()

#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
#         return response



'''

class UserView(APIView):



    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
        
'''



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


        return Response(
            data={
                "jwt": access_token,
                "refresh_token": refresh_token,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
    

class UserView(APIView):
    # permission_classes = [permissions.IsAuthenticated,]
    def get(self, request):
        print('++++++', dir(request), '++++++++++')
        print('++++++', request.data, '++++++++++')
        print('++++++', request.COOKIES, '++++++++++')

        
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)





'''   
    
        
        access_token = generate_access_token(user.id)
        # refresh_token = generate_refresh_token(user.id)

        refresh_token_obj, created = RefreshToken.objects.get_or_create(user=user)
        # refresh_token_obj.token = refresh_token
        # refresh_token_obj.expires_at = refresh_token_exp
        refresh_token_obj.save()
        

        return access_token
        
        
    '''

        # return Response(
        #     data={
        #         "access_token": str(access_token),
        #         # "refresh_token": str(refresh_token),
                
        #         "email": user.email,
        #     },
        #     status=status.HTTP_200_OK,
        # )
        

        # offset = datetime.timedelta(hours=-8)

        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + offset,
        #     'iat': datetime.datetime.utcnow()
        # }


        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta('utc-8'),
        #     'iat': datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload, 'secret', algorithm='HS256')

        # response = Response()

        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'jwt': token
        # }
        # return response


    

# class UserView(APIView):

#     def get(self, request):
#         print('request ---->', request.COOKIES)
#         token = request.COOKIES.get('jwt')
#         print('token ==================', token)

#         if not token:
#             print('++++++')
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, 'secret', algorithm=['HS256'])

#         except jwt.ExpiredSignatureError:
#             print('******')
#             raise AuthenticationFailed('Unauthenticated!')

#         user = CustomUser.objects.filter(id=payload['id']).first()
#         serializer = CustomUserSerializer(user)
#         return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response



        '''
        
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        # ___________________________________________________________
        # Допольнительная ифнормация о токене
        access_token_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        refresh_token_lifetime = api_settings.REFRESH_TOKEN_LIFETIME
        current_datetime = datetime.now()
        access_token_expiration = current_datetime + access_token_lifetime
        refresh_token_expiration = current_datetime + refresh_token_lifetime
        # ___________________________________________________________

        return Response(
            data={
                "access_token": str(access_token),
                "access_token_expires": access_token_expiration.strftime("%Y-%m-%d %H:%M:%S"),

                "refresh_token": str(refresh_token),
                "refresh_token_expires": refresh_token_expiration.strftime("%Y-%m-%d %H:%M:%S"),
                
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
        
        '''

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
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                data={"error": "Refresh token is required."}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as ex:
            log_error(self, ex)
            raise AuthenticationFailed("Invalid token.")

        return Response(
            "Logged out successfully", 
            status=status.HTTP_200_OK
            )  
    



from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view."})