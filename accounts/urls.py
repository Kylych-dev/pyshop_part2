from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import (
    AuthenticationView,
    RegisterView,
    UserView,
    LogoutView,
    protected_view,
    )

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls

urlpatterns.extend(
    [   
        path('register/', RegisterView.as_view({"post": "register"}), name='register'),
        path('login/', AuthenticationView.as_view({"post": "login"}), name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('user/', UserView.as_view()),
        path('protected/', protected_view, name='protected_view'),

    ]
)



'''
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserAuthenticationView


# router = DefaultRouter(trailing_slash=False)
# urlpatterns = router.urls





urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserAuthenticationView.as_view(), name='login'),
    path('logout/', UserAuthenticationView.as_view(), name='logout'),

]'''


'''
urlpatterns = [
    # Регистрация
    path("register/", RegisterView.as_view(), name="register"),
    
    # Логин и выход
    path("login/", UserAuthenticationView.as_view(), name="login"),
    path("logout/", UserAuthenticationView.as_view(), name="logout")
]'''