
from . import views

from django.urls import path

urlpatterns = [

    path('signup/', views.UserSignUpAPIView.as_view(), name='signup'),
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
   

]

