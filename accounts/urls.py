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
        path('register/', RegisterView.as_view({"post": "register"}), name='register'),
        path('login/', AuthenticationView.as_view({"post": "login"}), name='login'),
        path('logout/', AuthenticationView.as_view({"post": "logout"}), name='logout'),
        path('user/', UserView.as_view()),
    ]
)
