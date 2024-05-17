from django.urls import path
from rest_framework.routers import DefaultRouter


from apps.accounts.views import (
    RegisterView,
    AuthenticationView,
    UserView,
)
from apps.product.views import ProductViewSet


router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [
        # Authenticate
        path('register/', RegisterView.as_view({"post": "register"}), name='register_user'),
        path('login/', AuthenticationView.as_view({"post": "login"}), name='login_user'),
        path('logout/', AuthenticationView.as_view({"post": "logout"}), name='logout_user'),

        # User
        path('user/retrieve/', UserView.as_view(), name='retrieve_user'),
        path('user/update/', UserView.as_view(), name='update_user'),

        # Book
        path("product/", ProductViewSet.as_view({"get": "list"}), name="product-list"),
        path("product/create/", ProductViewSet.as_view({"post": "create"}), name="product-create"),
        path("product/<int:pk>/udpate/", ProductViewSet.as_view({"put": "update"}), name="product-update"),
        path("product/<int:pk>/destroy/", ProductViewSet.as_view({"delete": "destroy"}), name="book-delete"),

    ]
)

