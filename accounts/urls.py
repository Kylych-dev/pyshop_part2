from django.urls import path
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from accounts.views import (
    AuthenticationView,
    RegisterView,
    UserView,
    )

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [   
        path('register/', RegisterView.as_view({"post": "register"}), name='register_user'),
        path('login/', AuthenticationView.as_view({"post": "login"}), name='login_user'),
        path('logout/', AuthenticationView.as_view({"post": "logout"}), name='logout_user'),
        path('user/retrieve/', UserView.as_view(), name='retrieve_user'),
        path('user/update/', UserView.as_view(), name='update_user'),
    ]
)


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
