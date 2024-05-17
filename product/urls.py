from django.urls import path, include
from rest_framework import routers
from .views import ProductListCreate, ProductRetrieveUpdateDestroy
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroy.as_view(), name='product-retrieve-update-destroy')
    
]    

   

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
