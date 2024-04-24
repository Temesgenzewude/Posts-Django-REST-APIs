
from . import views

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [

    path('signup/', views.UserSignUpAPIView.as_view(), name='signup'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
   
    path('token/jwt/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('token/jwt/verify/', TokenVerifyView.as_view(), name='verify'),
    path('token/jwt/create/', TokenObtainPairView.as_view(), name='obtain-pair'),
   

]

