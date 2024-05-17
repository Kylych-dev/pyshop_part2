from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from datetime import datetime, timedelta
import uuid

from .manager import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, blank=True, null=True)
    password = models.CharField(_('password'), max_length=128)
    refresh_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        app_label = "accounts"

    def __str__(self):
        return self.email
    

class RefreshToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return self.expires_at < datetime.utcnow()

    def save(self, *args, **kwargs):
        self.expires_at = datetime.utcnow() + timedelta(days=7)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email




'''

RESTful API должен быть разработан с использованием Django и Django REST Framework.
 Токен доступа не хранится в базе данных;  это проверяется в конечных точках аутентификации без обращений к базе данных с использованием библиотеки PyJWT.

 Токен обновления должен храниться в базе данных со сроком действия и быть привязан к пользователю.  
 Это позволяет сделать токен недействительным при необходимости (например, когда пользователь выходит из системы).
 
 Используйте модуль django-constance для управления временем жизни токенов доступа и обновления.
 
 Документация по API: предоставьте доступный для просмотра API с документацией по конечным точкам.
 
 Тесты. 
 
 Рекомендуется модульные тесты и интеграционные тесты для вашего API.
 
 Развертывание. 
 
 Для демонстрации функциональности API вы можете использовать бесплатные хостинговые платформы, такие как Heroku, которые предлагают удобные средства для развертывания приложений Django.

 
 '''