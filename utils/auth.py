import jwt
from datetime import datetime, timedelta
from constance import config
from django.utils import timezone
from django.conf import settings
from rest_framework.response import Response
from accounts.models import RefreshToken



def generate_access_token(user_id):
    payload = {
        'id': user_id,
        'exp': timezone.now() + timedelta(minutes=60),
        'iat': timezone.now()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def generate_refresh_token(user_id):
    token = jwt.encode({'user_id': user_id}, str(settings.CONSTANCE_CONFIG['REFRESH_SECRET_KEY']), algorithm='HS256')
    refresh_token_obj, created = RefreshToken.objects.get_or_create(
        user_id=user_id, 
        defaults={'token': token, 'expires_at': timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION'])}
    )
    if not created:
        refresh_token_obj.expires_at = timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION'])
        refresh_token_obj.save()
    return token







# def generate_access_token(user_id):
#     payload = {
#         'id': user_id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#         'iat': datetime.datetime.utcnow()
#     }

#     token = jwt.encode(payload, 'secret', algorithm='HS256')
#     return token


# def generate_access_token(user_id):

#     payload = {
#             'id': user_id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow()
#         }


#     token = jwt.encode(payload, 'secret', algorithm='HS256')
#     response = Response()

#     response.set_cookie(key='jwt', value=token, httponly=True)
#     response.data = {
#         'jwt': token
#     }
#     return response



# def generate_refresh_token(user_id):
#     # Генерируем новый токен
#     token = jwt.encode({'user_id': user_id}, settings.CONSTANCE_CONFIG['REFRESH_SECRET_KEY'], algorithm='HS256')

#     # Проверяем, существует ли RefreshToken с таким токеном
#     refresh_token_obj = RefreshToken.objects.filter(token=token).first()

#     # Если RefreshToken с таким токеном уже существует, обновляем его
#     if refresh_token_obj:
#         refresh_token_obj.expires_at = timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION'])
#         refresh_token_obj.save()
#     else:
#         refresh_token_obj = RefreshToken.objects.create(
#             user_id=user_id, 
#             token=token, 
#             expires_at=timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION']))

#     return token

'''

def generate_refresh_token(user_id):
    # Проверяем, существует ли RefreshToken для данного пользователя
    refresh_token_obj, created = RefreshToken.objects.get_or_create(user_id=user_id)

    # Обновляем существующий RefreshToken или создаем новый
    if not created:
        refresh_token_obj.expires_at = timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION'])
        refresh_token_obj.save()
    else:
        payload = {
            'user_id': user_id,
            'exp': timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION']),
            'iat': timezone.now()
        }
        token = jwt.encode(payload, settings.CONSTANCE_CONFIG['REFRESH_SECRET_KEY'], algorithm='HS256')
        refresh_token_obj.token = token
        refresh_token_obj.save()

    return refresh_token_obj.token
'''

'''
def generate_refresh_token(user_id):

    payload = {
        'user_id': user_id,
        'exp': timezone.now() + timedelta(days=settings.CONSTANCE_CONFIG['REFRESH_TOKEN_EXPIRATION']),
        'iat': timezone.now()
    }



    return jwt.encode(payload, settings.CONSTANCE_CONFIG['REFRESH_SECRET_KEY'], algorithm='HS256')


'''



'''

def generate_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': timezone.now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRATION),  # Устанавливаем срок жизни токена (15 минут)
        'iat': timezone.now()  # Устанавливаем время создания токена
        # 'exp': datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRATION),  # Устанавливаем срок жизни токена (15 минут)
        # 'iat': datetime.utcnow()  # Устанавливаем время создания токена

    }
    return jwt.encode(payload, 'access_secret', algorithm='HS256')



def generate_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': timezone.now() + timedelta(minutes=config.REFRESH_TOKEN_EXPIRATION),  # Устанавливаем срок жизни токена (15 минут)
        'iat': timezone.now()  # Устанавливаем время создания токена
        # 'exp': datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_EXPIRATION),  # Устанавливаем срок жизни токена (7 дней)
        # 'iat': datetime.utcnow()  # Устанавливаем время создания токена
    }
    return jwt.encode(payload, 'refresh_secret', algorithm='HS256')

def refresh_tokens(access_token, refresh_token):
    access_payload = jwt.decode(access_token, 'access_secret', algorithms=['HS256'])
    refresh_payload = jwt.decode(refresh_token, 'refresh_secret', algorithms=['HS256'])

    # Проверяем, истек ли срок жизни токена доступа
    # if datetime.utcnow() > datetime.fromtimestamp(access_payload['exp']):
    if timezone.now() > datetime.fromtimestamp(access_payload['exp']):
    
        # Генерируем новый access token
        new_access_token = generate_access_token(refresh_payload['user_id'])

        # Обновляем refresh token (можно также перегенерировать refresh token, если требуется)
        new_refresh_token = refresh_token

        return new_access_token, new_refresh_token
    else:
        # Токен доступа еще действителен, возвращаем текущие токены
        return access_token, refresh_token
'''