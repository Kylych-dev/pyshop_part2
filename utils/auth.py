import jwt
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from apps.accounts.models import RefreshToken


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