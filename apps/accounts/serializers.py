from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'username',
            'refresh_token',
            'password'
            ]
        extra_kwargs = {
            'password': {'write_only': True}
            }




'''

{
    "id": 2,
    "email": "user2222@mail.ru",
    "last_login": null,
    "is_superuser": false,
    "first_name": "",
    "last_name": "",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2024-04-08T09:04:46.059773Z",
    "username": null,
    "refresh_token": "73048a28-a455-40a6-817f-74300ce481bc",
    "groups": [],
    "user_permissions": []
}
'''
