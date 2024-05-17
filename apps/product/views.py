from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        # method='get',
        operation_description='Получение списка продуктов',
        operation_id='list_products',
        operation_summary='Список продуктов',
        tags=['Product'],
        responses={
            200: openapi.Response(description='OK'),
            400: openapi.Response(description='Bad Request'),
        },
    )
    @action(detail=False, methods=['get'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        # method='post',
        operation_description='Создание нового продукта',
        operation_summary='Создание продукта',
        operation_id='create_product',
        tags=['Product'],
        responses={
            201: openapi.Response(description='Created - Продукт успешно создан'),
            400: openapi.Response(description='Bad Request - Неверный запрос'),
        },
    )
    @action(detail=False, methods=['post'])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        # method='get',
        operation_description='Получение данных продукта',
        operation_summary='Получение данных продукта',
        operation_id='retrieve_product',
        tags=['Product'],
        responses={
            200: openapi.Response(description='OK'),
            404: openapi.Response(description='Not Found - Ресурс не найден'),
        },
    )
    @action(detail=True, methods=['get'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        # method='put',
        operation_description='Обновление данных продукта',
        operation_summary='Обновление продукта',
        operation_id='update_product',
        tags=['Product'],
        responses={
            200: openapi.Response(description='OK - Продукт успешно обновлен'),
            400: openapi.Response(description='Bad Request - Неверный запрос'),
            404: openapi.Response(description='Not Found - Ресурс не найден'),
        },
    )
    @action(detail=True, methods=['put'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        # method='delete',
        operation_description='Удаление продукта',
        operation_summary='Удаление продукта',
        operation_id='delete_product',
        tags=['Product'],
        responses={
            204: openapi.Response(description='No Content - Продукт успешно удален'),
            404: openapi.Response(description='Not Found - Ресурс не найден'),
        },
    )
    @action(detail=True, methods=['delete'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
