from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Создаем роутер и регистрируем наш ProductViewSet
router = DefaultRouter()
router.register(r'products', ProductViewSet)

# Определяем маршруты
urlpatterns = [
    path('', include(router.urls)),
]

# Настройка для Swagger и Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="Product API",
        default_version='v1',
        description="API for managing products",
    ),
    public=True,
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]