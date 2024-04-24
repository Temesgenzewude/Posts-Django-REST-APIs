from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from .serializers import UserSignUpSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import get_object_or_404
from .models import User
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class UserSignUpAPIView(generics.GenericAPIView):

    serializer_class = UserSignUpSerializer
    permission_classes=[]

    def post(self, request:Request):
        data= request.data
        serializer = self.serializer_class(data= data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'You have successfully signed up!',
                'data': serializer.data
            }
            return Response(data= response, status=status.HTTP_201_CREATED)
        else:
            return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginAPIView(generics.GenericAPIView):

    permission_classes=[]

    def post(self, request:Request):
        email= request.data.get('email')
        password= request.data.get('password')

        if not email:
            return Response(data= {'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response(data= {'message': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        # find the user in the database using the email

        # user= get_object_or_404(User, email=email)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response(data={'message': 'User with the give email not found!'}, status=status.HTTP_404_NOT_FOUND)

        
        # try:
        #     user= User.objects.get(email=email)
        #     print(user)
        # except User.DoesNotExist:
        #     return Response(data= {'message': 'User with the given email doesn\'t exist!'}, status=status.HTTP_404_NOT_FOUND)
        
        user= authenticate(email=email, password=password)

        if not user:
            return Response(data= {'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token= RefreshToken.for_user(user)

        print("Refresh token is " + str(refresh_token))
        print("Access token is " + str(refresh_token.access_token))
        

        if refresh_token is not None:
            response= {
                'message': 'You have successfully logged in!',
                'data': {
                    'id': user.id,
                    'email': user.email,

                    'username': user.username,
                    'date_of_birth': user.date_of_birth,
                    'access_token': str(refresh_token.access_token),
                    'refresh_token': str(refresh_token)

                }
            }
            return Response(data= response, status=status.HTTP_200_OK)
        
        else:
            return Response(data= {'message': 'Invalid credentials provided!'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request:Request):

        contents={
            "user": str(request.user),
            "auth_token": str(request.auth)

        }

        return Response(data= contents, status=status.HTTP_200_OK)
        
    
