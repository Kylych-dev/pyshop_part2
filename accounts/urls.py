from django.urls import path
from rest_framework.routers import DefaultRouter

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
